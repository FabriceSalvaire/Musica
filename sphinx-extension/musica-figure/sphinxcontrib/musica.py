####################################################################################################
#
# Musica - A Music Theory package for Python
# Copyright (C) 2017 Salvaire Fabrice
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

"""This plugin provides a figure directive for Sphinx Documentation Generator.

"""

####################################################################################################

# from hashlib import sha1 as sha
import os
from os import path

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from Musica.Figure.Render import render_figure as _render_figure

####################################################################################################

def render_figure(self, figure_cls, kwargs, figure_name, extensions):

    # self.builder.warn('Render figure')
    # print('>>> Musica Render figure', figure_cls, kwargs, figure_name, extensions)

    # shasum = sha().hexdigest()

    # .../_images/musica_figure/foo.svg
    extension = '.svg' # Fixme: ok ???
    relative_filename = path.join(self.builder.imgpath, 'musica_figure', figure_name + extension)
    # to get absolute path
    absolute_filename = path.join(self.builder.outdir, '_images', 'musica_figure', figure_name + extension)
    # print('>>> Musica', relative_filename, absolute_filename)

    dst_directory = path.dirname(absolute_filename)
    if not path.exists(dst_directory):
        os.mkdir(dst_directory)

    if not path.exists(absolute_filename):
        absolute_filename_base, ext = path.splitext(absolute_filename)
        # print(absolute_filename_base)
        for extension in extensions:
            _render_figure(
                figure=figure_cls,
                kwargs=kwargs,
                output=absolute_filename_base + extension,
                # paper=paper,
                # margin=margin,
                # dvisvgm=margin,
            )

    # print("exit musica.render_figure")

    return relative_filename

####################################################################################################

# fixme: Part ???

class MusicaFigure(nodes.Part, nodes.Element):
    pass

####################################################################################################

class MusicaFigureDirective(Directive):

    """ This class defines a ``musica-figure`` directive.

    .. musica-figure:: ReST

        .. musica-figure::  guitare-fretboard  Musica.Figure.Fretboard.FretboardFigure
            :kwargs: instrument='Guitar',tuning='Standard
            :extensions: svg,tex,pdf

    """

    ##############################################

    align_h_values = ('left', 'center', 'right')
    align_v_values = ('top', 'middle', 'bottom')
    align_values = align_v_values + align_h_values

    ##############################################

    @classmethod
    def align(cls, argument):
        # This is not callable as self.align.  We cannot make it a staticmethod because we're saving
        # an unbound method in option_spec below.
        return directives.choice(argument, cls.align_values)

    ##############################################

    has_content = False
    required_arguments = 2
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        'kwargs': directives.unchanged,
        'extensions': directives.unchanged, # Fixme: .split(',') ...
        'alt': directives.unchanged,
        'height': directives.length_or_unitless,
        'width': directives.length_or_percentage_or_unitless,
        # 'scale': directives.percentage,
        'align': align,
    }

    ##############################################

    def run(self):

        # print('>>> MusicaFigureDirective.run', self.block_text, self.arguments, self.options)
        node = MusicaFigure()
        node['figure_name'] = self.arguments[0]
        node['figure_cls'] = self.arguments[1]
        node['kwargs'] = self.options.get('kwargs', '')
        node['extensions'] = self.options.get('extensions', ('.tex', '.pdf', '.svg'))
        node['center'] = self.options.get('align', 'center')

        for key in ('width', 'height'):
            if key in self.options:
                node[key] = self.options[key]

        return [node]

####################################################################################################

def visit_MusicaFigure_html(self, node):

    # print('>>> visit_MusicaFigure_html')

    try:
        filename = render_figure(self,
                                 figure_cls=node['figure_cls'],
                                 kwargs=node['kwargs'],
                                 figure_name=node['figure_name'],
                                 extensions=node['extensions'],
        )
    except Exception as exception:
        print('Error:', exception) # Fixme
        sytem_message = nodes.system_message(str(exception), type='WARNING', level=2,
                                             backrefs=[], source=node['figure_name'])
        sytem_message.walkabout(self)
        self.builder.warn('inline musica figure {}'.format(node['figure_name'] + str(exception)))
        raise nodes.SkipNode

    self.body.append(self.starttag(node, 'div', CLASS='musica-figure'))
    if filename is None:
        # Fixme: then exception is raised ...
        # something failed -- use text-only as a bad substitute
        self.body.append('<span>failed to generate {}</span>'.format(self.encode(node['figure_name'])))
    else:
        filename_base, ext = path.splitext(filename)
        # Fixme: svgz
        if '.svg' in node['extensions']:
            kwargs = {'src': filename_base + '.svg'}
            if 'width' in node:
                kwargs['width'] = node['width']
            if 'height' in node:
                kwargs['height'] = node['height']
            if 'alt' in node:
                kwargs['alt'] = node['alt']
            if 'align' in node:
                self.body.append('<div align="%s" class="align-%s">' % (node['align'], node['align']))
                self.context.append('</div>\n')
            # else:
            #     self.context.append('')
            self.body.append(self.emptytag(node, 'img', '', **kwargs))

            pattern = '<li><a href="{}"><i class="fa {} fa-2x"></i></a></li>'
            self.body.append('<div class="musica-figure-download">')
            self.body.append('<ul>')
            self.body.append(pattern.format(filename_base + '.svg', 'fa-file-o'))
            self.body.append(pattern.format(filename_base + '.tex', 'fa-file-text-o'))
            self.body.append(pattern.format(filename_base + '.pdf', 'fa-file-pdf-o'))
            self.body.append('</ul></div>\n')

    raise nodes.SkipNode

####################################################################################################

def depart_MusicaFigure_html(self, node):
    self.body.append(self.context.pop())

####################################################################################################

def setup(app):

    # print('>>> Musica setup')

    app.add_node(MusicaFigure,
                 html=(visit_MusicaFigure_html, depart_MusicaFigure_html),
                 )

    app.add_directive('musica-figure', MusicaFigureDirective)
