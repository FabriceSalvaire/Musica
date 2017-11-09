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
    'Fretboard',
]

####################################################################################################

import math

from ..Geometry.Path import Polyline
from ..Geometry.Transformation import AffineTransformation2D
from ..Geometry.Vector import Vector2D
# from ..Instrument.InstrumentDatabase import InstrumentDatabase
from ..Instrument.StringInstrument import StringInstrumentTuningDatabase, String # , StringTuning
from ..Tex.Tikz import TikzFigure, Coordinate
from ..Theory.Pitch import Pitch

####################################################################################################

class Fretboard(TikzFigure):

    ##############################################

    def __init__(self, **kwargs):


        tuning = kwargs['tuning']
        if isinstance(tuning, str): # not StringTuning
            tuning_database = StringInstrumentTuningDatabase.instance()
            instrument = kwargs['instrument']
            tuning = tuning_database[instrument][tuning]

        reverse = kwargs.get('reverse', False)
        # Fixme: Guitare default
        number_of_frets = kwargs.get('number_of_frets', 12)
        diapason = kwargs.get('diapason', 640) # mm

        number_of_strings = tuning.number_of_strings

        string0 = String(tuning[0], diapason)
        x_last_fret = string0.fret_position(number_of_frets)

        # Fixme: scale, paper
        super().__init__(options='x=.5mm,y=5mm')

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(4)

        # Fixme: broken corner

        # Mark
        #   circle: 3, 5, 7, 9, 15, 17
        #   2 circles: 12

        # Fret 0 is at 0
        fret_positions = [string0.fret_position(i)
                          for i in range(number_of_frets +1)]

        for i in range(number_of_strings +1):
            y = i
            if i == 0 or i == number_of_strings:
                linewidth = '1pt'
            else:
                linewidth = '.5pt'
            point0 = Vector2D(0, i)
            point1 = Vector2D(x_last_fret, i)
            self.line(point0, point1, linewidth=linewidth)
            if 0 <= i < number_of_strings:
                y_middle = y + .5
                point = Vector2D(-1, y_middle)
                self.text(point, i+1, anchor='east')
                point = Coordinate('-6em', y_middle)
                pitch = tuning[i]
                english_pitch = pitch.unicode_name_with_octave
                latin_pitch = pitch.latin_unicode_name_with_octave
                self.text(point, '{} / {}'.format(english_pitch, latin_pitch), anchor='west')
                fret_pitch = pitch.clone()
                for i in range(number_of_frets):
                    fret_pitch = fret_pitch.next_pitch()
                    x = (fret_positions[i] + fret_positions[i+1]) / 2
                    point = Coordinate(x, y_middle)
                    english_pitch = fret_pitch.unicode_name_with_octave
                    latin_pitch = fret_pitch.latin_unicode_name
                    self.text(point, '{} / {}'.format(english_pitch, latin_pitch))

        for i in range(number_of_frets +1):
            x = fret_positions[i]
            point0 = Vector2D(x, 0)
            point1 = Vector2D(x, number_of_strings)
            if i == 0:
                linewidth = '4pt'
            else:
                linewidth = '1pt'
            self.line(point0, point1, linewidth=linewidth)
            if 0 < i < (number_of_frets + 1):
                x_middle = (x + string0.fret_position(i-1)) / 2
                point = Vector2D(x_middle, -.25)
                self.text(point, i, anchor='north')
