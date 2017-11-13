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

import importlib
import logging
import os

from Musica.Tex.Document import Document
from Musica.Tex.Package import Package
# from Musica.Tex.Tikz import TikzFigure

####################################################################################################

_logger = logging.getLogger(__name__)

####################################################################################################

def timestamp(path):
    return os.stat(path).st_ctime

####################################################################################################

def render_figure(figure,
                  kwargs,
                  output,
                  paper='a4paper',
                  margin=10,
                  dvisvgm=False,
                  force=False):

    parts = figure.split('.')
    figure_module = importlib.import_module('.'.join(parts[:-1]))
    figure_class = getattr(figure_module, parts[-1])

    if (not force
        and os.path.exists(output)
        and timestamp(figure_module.__file__) <= timestamp(output)):
        return

    if dvisvgm:
        tex_document = Document(class_name='minimal', class_options=('dvisvgm',))
    else:
        tex_document = Document(class_name='article', class_options=(paper,))

        tex_document.append_preambule(r'''
        \RequirePackage{luatex85} % for geometry
        ''')

        tex_document.packages.add(Package('geometry',
                                          'includeheadfoot',
                                          paper=paper,
                                          margin='1cm',
                                          # headsep='1cm',
                                          # footskip='1cm',
        ))

        tex_document.empty_page_style()

    # TikzFigure.setup_externalisation(tex_document)

    kwargs = eval('dict(' + kwargs + ')')
    _logger.info(kwargs)

    figure = figure_class(**kwargs)
    tex_document.append(figure)

    # print(str(tex_document))
    tex_document.generate(output, crop=True, margin=margin, dvisvgm=dvisvgm)
