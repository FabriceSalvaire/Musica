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

from . import Environment
from . import Document

####################################################################################################

class Tabular(Environment):

    #######################################

    def __init__(self, tabular_format,
                 position='',
                 environment='tabular',
                 alternated_colour=False,
                 colour_model='gray',
                 odd_row_colour='.9',
                 even_row_colour='1.',
                 ):

        super(Tabular, self).__init__(name=environment)

        self.format = tabular_format
        self.position = position
        self.alternated_colour = alternated_colour
        self.colour_model = colour_model
        self.odd_row_colour = odd_row_colour
        self.even_row_colour = even_row_colour

        self._odd_row = True

    #######################################

    def set_begin(self):

        self.begin_buffer.push(r'\begin{%s}[%s]{%s}' % (self.name, self.position, self.format) + '\n')

    #######################################

    def push_columns(self, columns, vspace=None):

        if self.alternated_colour:
            self.set_odd_even_row_colour(self._odd_row)
            self._odd_row = not self._odd_row

        line_break = Document.LINE_BREAK
        if vspace is not None:
            line_break += '[%s]' % (vspace)
        self.push(' & '.join(columns) + ' ' + line_break + '\n')

    #######################################

    def hline(self):

        self.push(r'\hline' + '\n')

    #######################################

    def set_row_colour(self, colour_model, colour):

        self.push(r'\rowcolor' + '[%s]{%s}' % (colour_model, colour)  + '\n')

    #######################################

    def set_odd_even_row_colour(self, odd_row):

        row_colour = self.odd_row_colour if odd_row else self.even_row_colour
        self.set_row_colour(self.colour_model, row_colour)
