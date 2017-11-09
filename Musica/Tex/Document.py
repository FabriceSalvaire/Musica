####################################################################################################
#
# Musica - A Music Theory Package for Python
# Copyright (C) 2017 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import logging
import os
import shutil
import subprocess
import tempfile

from .Buffer import TexContent
from .Environment import Environment
from .Package import Package

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

class Document(TexContent):

    _logger = _module_logger.getChild('Document')

    #######################################

    def __init__(self, class_name, class_options=()):

        super().__init__()

        self._class_name = class_name
        self._class_options = class_options

        self.packages.add(Package('fontspec'))

    ##############################################

    def __str__(self):

        class_options = ', '.join(self._class_options)
        source = self.format(r'\documentclass[«1»]{«0._class_name»}', self, class_options) + '\n'

        packages = self.collect_packages()
        for package in packages:
            source += str(package) + '\n'

        source += self.collect_preambule()

        source += r'\begin{document}' + '\n'
        source += self.to_string('content')
        source += r'\end{document}' + '\n'

        return source

    ##############################################

    @staticmethod
    def _make_filename(path, filename, extension):

        return os.path.join(path, filename + '.' + extension)

    #######################################

    # Fixme: use shell ???
    __latex_command__ = '/usr/bin/lualatex'
    __pdfcrop_command__ = '/usr/bin/pdfcrop'
    __svg_command__ = '/usr/bin/pdf2svg'
    __dvisvgm_command__ = '/usr/bin/dvisvgm'

    def generate(self, output_path, crop=False, margin=10, dvisvgm=False):

        if dvisvgm and not output_path.stopswith('.svg'):
            raise ValueError("Output must be SVG when using dvisvgm")

        output_path = os.path.abspath(output_path)
        base, extension = os.path.splitext(output_path)
        extension = extension[1:]
        output_dir = os.path.dirname(base)
        filename = os.path.basename(base)
        self._logger.info("Output is {} {} {}".format(output_dir, filename, extension))

        if not os.path.exists(output_dir):
            raise NameError("Output directory {} don't exists".format(output_dir))

        with tempfile.TemporaryDirectory() as tmp_dir:
            self._logger.info("Temporary directory is {}".format(tmp_dir))

            if extension == 'tex':
                tex_path = self._make_filename(output_dir, filename, 'tex')
                self._logger.info('Write {}'.format(tex_path))
            else:
                tex_path = self._make_filename(tmp_dir, 'out', 'tex')
            with open(tex_path, 'w') as fd:
                fd.write(str(self))

            if extension in ('pdf', 'svg'):
                pdf_path = self._make_filename(tmp_dir, 'out', 'pdf')

                command = [
                    self.__latex_command__,
                    '--interaction=batchmode',
                    '--shell-escape',
                    '--output-directory={}'.format(tmp_dir), # self.output_directory
                ]
                if dvisvgm:
                    command.append('--output-format=dvi')
                command.append(tex_path)
                subprocess.call(command)

                if os.path.exists(pdf_path):
                    if dvisvgm:
                        dvi_path = self._make_filename(tmp_dir, 'out', 'dvi')
                        dst_path = self._make_filename(output_dir, filename, 'svg')
                        command = (
                            self.__dvisvgm_command__,
                            '--output={}'.format(dst_path),
                            '--zip=9',
                            '--no-fonts',
                            # '--font-format=woff,autohint',
                            dvi_path,
                        )
                        subprocess.call(command)
                    else:
                        if crop:
                            cropped_pdf_path = self._make_filename(tmp_dir, 'out-crop', 'pdf')
                            subprocess.call((self.__pdfcrop_command__, '--margins', str(margin), pdf_path, cropped_pdf_path))
                            pdf_path = cropped_pdf_path
                        if extension == 'pdf':
                            dst_path = self._make_filename(output_dir, filename, 'pdf')
                            # os.rename(pdf_path, dst_path)
                            shutil.copyfile(pdf_path, dst_path)
                        elif extension == 'svg':
                            dst_path = self._make_filename(output_dir, filename, 'svg')
                            subprocess.call((self.__svg_command__, pdf_path, dst_path))
                            # mutool draw -o output input
                else:
                    raise NameError("LaTeX failed")
