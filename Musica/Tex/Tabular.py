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

from .Environment import Environment
from .Buffer import Buffer
from .Package import Package

####################################################################################################

class Tabular(Environment):

    #######################################

    def __init__(self, tabular_format,
                 position='', # ('h', 't', 'b', 'p')
                 environment='tabular',
                 ):

        super().__init__(name=environment, options=position)

        self.packages.add(Package('multirow'))
        self.packages.add(Package('xcolor', 'table'))

        self._format = tabular_format

    #######################################

    def format_begin(self):

        return super().format_begin() + '{%s}' % self._format

    #######################################

    def end_row(self, vspace=None):

        line_break = Buffer.LINE_BREAK # Fixme:
        if vspace is not None:
            line_break += '[{}]'.format(vspace)
        self.append(' ' + line_break)

    #######################################

    def add_row(self, columns, vspace=None):

        self.append(' & '.join(columns), newline=False)
        self.end_row(vspace)

    #######################################

    @staticmethod
    def multicolumn(number_of_columns, column_format, content):

        # Fixme:
        return Tabular.format(r'\multicolumn{«0»}{«1»}{«2»}', number_of_columns, column_format, content)

    #######################################

    def hline(self):

        self.append(r'\hline')

    #######################################

    def set_row_colour(self, colour):

        # self.append(self.format(r'\rowcolor[«0»]{«1»}', colour_model, colour))
        self.append(self.format(r'\rowcolor{«0»}', colour))

####################################################################################################

#class AlternatedColourTabular(Environment):
#
#    #######################################
#
#    def __init__(self, tabular_format,
#                 position='',
#                 environment='tabular',
#                 alternated_colour=False,
#                 colour_model='gray',
#                 odd_row_colour='.9',
#                 even_row_colour='1.',
#                 ):
#
#        ...
#
#        self._alternated_colour = alternated_colour
#        self._colour_model = colour_model
#        self._odd_row_colour = odd_row_colour
#        self._even_row_colour = even_row_colour
#        self._odd_row = True
#
#    #######################################
#
#    def add_row(self, columns, vspace=None):
#
#        if self._alternated_colour:
#            self._set_odd_even_row_colour(self._odd_row)
#            self._odd_row = not self._odd_row
#
#        ...
#
#    #######################################
#
#    def _set_odd_even_row_colour(self, odd_row):
#
#        row_colour = self._odd_row_colour if odd_row else self._even_row_colour
#        self.set_row_colour(self._colour_model, row_colour)
