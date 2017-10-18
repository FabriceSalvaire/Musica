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

__all__ = [
    'FrequencyTable',
    ]

####################################################################################################

from Musica.Tex.Buffer import TexContent
from Musica.Tex.Environment import Center
from Musica.Tex.Tabular import Tabular
from Musica.Theory.Pitch import Pitch

####################################################################################################

class FrequencyTable(Tabular):

    ##############################################

    def __init__(self,
                 octave_inf=0,
                 octave_sup=10):

        tabular_format = '|' + '|'.join(['r', 'c', 'c'] + ['r']*(octave_sup - octave_inf +1)) + '|'

        super().__init__(tabular_format)

        # self.preambule.set_main_font('Latin Modern Sans') # Roman
        # self.preambule.font_size(12)

        octaves = range(octave_inf, octave_sup+1)

        self.hline()
        self.add_row(['']*3 + [self.multicolumn(1, 'c|', str(x)) for x in octaves])
        self.hline()

        for step in range(12):
            frequencies = [Pitch(step, octave=octave).frequency for octave in octaves]
            pitch = Pitch(step)
            english_note = pitch.english_locale.tex_name
            latin_note = pitch.french_locale.tex_name
            if pitch.alteration:
                self.set_row_colour('gray!30')
                english_note += '/' + pitch.english_locale.tex_flat_name
                latin_note += '/' + pitch.french_locale.tex_flat_name
            else:
                self.set_row_colour('gray!0')
            columns = [str(step + 1), latin_note, english_note]
            columns += ['{:.1f}'.format(frequency) for frequency in frequencies]
            self.add_row(columns)
            self.hline()

####################################################################################################

class FrequencyTablePage(TexContent):

    ##############################################

    def __init__(self):

        super().__init__()

        self.centerline(r'\Huge{Frequencies Table}')
        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(12)
        center = Center()
        center.append(FrequencyTable())
        self.append(center)
