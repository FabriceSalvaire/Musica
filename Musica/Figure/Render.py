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

import datetime
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

    header = '''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% This LaTeX source file
% is part of the Musica Toolkit https://musica.fabrice-salvaire.fr
% and licensed under CC BY-NC-SA 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''

    if dvisvgm:
        class_options = ['dvisvgm']
    else:
        class_options = [paper]

    tex_document = Document(
        class_name='minimal',
        class_options=class_options,
        header=header.lstrip()
    )

    if not dvisvgm:
        tex_document.append_preambule(r'\RequirePackage{luatex85} % for geometry')
        tex_document.packages.add(Package('geometry',
                                          'includeheadfoot',
                                          paper=paper,
                                          margin='1cm',
                                          # headsep='1cm',
                                          # footskip='1cm',
        ))

    # TikzFigure.setup_externalisation(tex_document)

    now = datetime.datetime.now()

    # Fixme: don't work
    pdfinfo_template = r'''
\protected\def\pdfinfo{{\pdfextension info}}
\pdfinfo{{
/Title ({title})
/Author ({author})
}}
'''
    tex_document.append_preambule(pdfinfo_template.format(
        title=figure,
        date=now,
        source='https://musica.fabrice-salvaire.fr',
        author='Musica Tookit',
        rights='http://creativecommons.org/licenses/by-nc-sa/4.0/',
    ))

    kwargs = eval('dict(' + kwargs + ')')
    _logger.info(kwargs)

    tex_figure = figure_class(**kwargs)
    tex_figure.add_license()
    tex_document.append(tex_figure)

    # print(str(tex_document))
    tex_document.generate(output, crop=True, margin=margin, dvisvgm=dvisvgm)

    if output.endswith('.svg'):
        with open(output, 'r') as fh:
            source = fh.read()
        position = source.find('>')
        position = source.find('>', position +1)
        metadata_template = '''
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
>
  <title id="title1">{title}</title>
  <metadata id="metadata1">
    <rdf:RDF>
      <cc:Work rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title>{title}</dc:title>
        <cc:license rdf:resource="http://creativecommons.org/licenses/by-nc-sa/4.0/" />
        <dc:creator><cc:Agent><dc:title>Musica Tookit</dc:title></cc:Agent></dc:creator>
        <dc:date>{date}</dc:date>
        <dc:source>{source}</dc:source>
        <dc:rights><cc:Agent><dc:title>{rights}</dc:title></cc:Agent></dc:rights>
        <dc:publisher><cc:Agent><dc:title>{publisher}</dc:title></cc:Agent></dc:publisher>
        <dc:identifier></dc:identifier>
        <dc:relation></dc:relation>
        <dc:language></dc:language>
        <dc:subject><rdf:Bag>
            <rdf:li></rdf:li>
            </rdf:Bag></dc:subject>
        <dc:coverage></dc:coverage>
        <dc:description>{description}</dc:description>
        <dc:contributor><cc:Agent><dc:title>{contributor}</dc:title></cc:Agent></dc:contributor>
      </cc:Work>
        <cc:License   rdf:about="https://creativecommons.org/licenses/by-nc-sa/4.0/">
        <cc:permits   rdf:resource="https://creativecommons.org/ns#Reproduction" />
        <cc:permits   rdf:resource="https://creativecommons.org/ns#Distribution" />
        <cc:requires  rdf:resource="https://creativecommons.org/ns#Notice" />
        <cc:requires  rdf:resource="https://creativecommons.org/ns#Attribution" />
        <cc:prohibits rdf:resource="https://creativecommons.org/ns#CommercialUse" />
        <cc:permits   rdf:resource="https://creativecommons.org/ns#DerivativeWorks" />
        <cc:requires  rdf:resource="https://creativecommons.org/ns#ShareAlike" />
      </cc:License>
    </rdf:RDF>
  </metadata>
'''
        metadata = metadata_template.format(
            title=figure,
            date=now,
            source='https://musica.fabrice-salvaire.fr',
            publisher='Musica Tookit',
            rights='http://creativecommons.org/licenses/by-nc-sa/4.0/',
            description='',
            contributor='',
        )
        with open(output, 'w') as fh:
            fh.write(source[:position])
            fh.write(metadata)
            fh.write(source[position+2:]) # skip \n
