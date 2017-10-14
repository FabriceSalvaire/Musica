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

import os
import subprocess

####################################################################################################

from . import Buffer, Environment

####################################################################################################

LINE_BREAK = r'\\'

####################################################################################################

class Document(object):

    #######################################

    def __init__(self, file_name, style, style_options=''):

        if file_name.endswith('.tex'):
            file_name = file_name[:-4]

        self._file_name = file_name
        self._style = style
        self._style_options = style_options

        self.preambule = Buffer()
        self.content = Environment(name='document')

    #######################################

    @property
    def tex_file_name(self):
        return self._file_name + '.tex'

    @property
    def output_directory(self):
        return os.path.dirname(self.tex_file_name())

    @property
    def pdf_file_name(self):
        return self._file_name + '.pdf'

    #######################################

    def newpage(self):

        self.content.push(r'\newpage' + '\n')

    #######################################

    def write(self):

        with open(self.tex_file_name, 'w') as stream:
            stream.write(r'\documentclass[%s]{%s}' % (self._style_options, self._style) + '\n')
            self.preambule.write(stream)
            stream.write('\n% Document content\n\n')
            self.content.write(stream)
        stream.close()

    #######################################

    def run_pdflatex(self):

        command = [
            'pdflatex',
            '--interaction=batchmode',
            '--output-directory={}'.format(self.output_directory),
            self.tex_file_name,
            ]
        subprocess.call(command, shell=True)
