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

from ArithmeticInterval import IntervalInt

from ..Geometry.Path import Polyline
from ..Geometry.Transformation import AffineTransformation2D
from ..Geometry.Vector import Vector2D
# from ..Instrument.InstrumentDatabase import InstrumentDatabase
from ..Instrument.StringInstrument import StringInstrumentTuningDatabase, String # , StringTuning
from ..Tex.Tikz import TikzFigure, Coordinate
from ..Theory.Pitch import Pitch

####################################################################################################

class StringFretboard:

    ##############################################

    def __init__(self, string, number_of_frets):

        self._string = string
        self._number_of_frets = number_of_frets

        pitch = string.pitch
        self._pitches = []
        for i in range(self._number_of_frets +1):
            self._pitches.append(pitch)
            pitch = pitch.next_pitch()

    ##############################################

    @property
    def string(self):
        return self._string

    @property
    def number_of_frets(self):
        return self._number_of_frets

    @property
    def pitch(self):
        return self._pitches[0]

    @property
    def pitch_interval(self):
        # /!\ midi note, i.e. int not float
        return IntervalInt(int(self._pitches[0]), int(self._pitches[-1]))

    ##############################################

    def __getitem__(self, i):
        return self._pitches[i]

####################################################################################################

class Fretboard:

    ##############################################

    def __init__(self, **kwargs):

        tuning = kwargs['tuning']
        if isinstance(tuning, str): # not StringTuning
            tuning_database = StringInstrumentTuningDatabase.instance()
            instrument = kwargs['instrument']
            tuning = tuning_database[instrument][tuning]

        # Fixme:
        reverse = kwargs.get('reverse', False)

        # Fixme: Guitare default
        self._diapason = kwargs.get('diapason', 640) # mm
        self._number_of_frets = kwargs.get('number_of_frets', 12)

        self._number_of_strings = tuning.number_of_strings
        self._strings = [StringFretboard(String(tuning[i], self._diapason), self._number_of_frets)
                         for i in self.string_iter]

        string0 = self._strings[0].string
        self._fret_positions = [string0.fret_position(i) for i in self.nut_fret_iter]

    ##############################################

    @property
    def number_of_strings(self):
        return self._number_of_strings

    @property
    def diapason(self):
        return self._diapason

    @property
    def number_of_frets(self):
        return self._number_of_frets

    @property
    def string_iter(self):
        return range(self._number_of_strings)

    @property
    def string_fretboard_iter(self):
        return iter(self._strings)

    @property
    def nut_fret_iter(self):
        return range(self._number_of_frets + 1)

    @property
    def fret_iter(self):
        return range(1, self._number_of_frets + 1)

    @property
    def x_last_fret(self):
        return self._fret_positions[-1]

    ##############################################

    def string(self, i):
        return self._strings[i]

    ##############################################

    def fret_position(self, i):
        return self._fret_positions[i]

    ##############################################

    def middle_position(self, i):
        return (self._fret_positions[i-1] + self._fret_positions[i]) / 2

####################################################################################################

class StringPart(IntervalInt):

    ##############################################

    def __init__(self, *args, strings=()):

        super().__init__(*args)
        if isinstance(strings, int):
            strings = (strings,)
        self.strings = set(strings)

    ##############################################

    def __and__(self, i2):

        intersection = super().__and__(i2)
        strings = set(self.strings)
        strings.update(i2.strings)

        return self.__class__(intersection, strings=strings)

    ##############################################

    def __str__(self):
        return super().__str__() +  str(self.strings)

####################################################################################################

def interval_parts(interval, sub_interval):

    # cases
    # 1 interval left | sub_interval
    # 2 interval left | sub_interval | interval right
    # 3                 sub_interval | interval right
    # 4          sub_interval == interval

    if interval == sub_interval: # 4
        return sub_interval
    elif interval.inf < sub_interval.inf:
        part1 = StringPart(interval.inf, sub_interval.inf -1, strings=interval.strings)
        part2 = sub_interval
        if sub_interval.sup < interval.sup: # 2
            part3 = StringPart(sub_interval.sup +1, interval.sup, strings=interval.strings)
            return part1, part2, part3
        else: # 1
            return part1, part2
    else: # sub_interval.inf <= interval.inf
        if sub_interval.sup < interval.sup: # 3
            part2 = StringPart(sub_interval.sup +1, interval.sup, strings=interval.strings)
            return sub_interval, part2
        else: # 4
            raise NotImplementedError # should not happen

####################################################################################################

def merge_parts(parts1, parts2):

    parts = {}
    for part in list(parts1) + list(parts2):
        if part not in parts:
            parts[part] = part
        else:
            parts[part].strings.update(part.strings)

    return parts.values()

####################################################################################################

def intersection_parts(interval1, interval2):

    if interval1.intersect(interval2):
        intersection = interval1 & interval2
        parts1 = interval_parts(interval1, intersection)
        parts2 = interval_parts(interval2, intersection)
        return merge_parts(parts1, parts2)
    else:
        return ()

####################################################################################################

class FretboardFigure(TikzFigure, Fretboard):

    ##############################################

    def __init__(self, **kwargs):

        Fretboard.__init__(self, **kwargs)

        parts = []
        for i in self.string_iter:
            string1_interval = self.string(i).pitch_interval
            for j in self.string_iter:
                if j != i:
                    string2_interval = self.string(j).pitch_interval
                    if string1_interval.intersect(string2_interval):
                        new_parts = intersection_parts(StringPart(string1_interval, strings=i),
                                                    StringPart(string2_interval, strings=j))
                        parts = merge_parts(parts, new_parts)
                        intersection = string1_interval & string2_interval
                        print(i, j, string1_interval, string2_interval, '&', intersection, 'P', ' '.join([str(x) for x in new_parts]))
        for interval in sorted(parts, key=lambda x: x.inf):
            print(interval)

        # Fixme: scale, paper
        TikzFigure.__init__(self, options='x=.5mm,y=5mm')

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(3)

        # Fixme: broken corner

        # Mark
        #   circle: 3, 5, 7, 9, 15, 17
        #   2 circles: 12

        # Paint string borders
        for i in range(self.number_of_strings +1):
            y = i
            if i == 0 or i == self.number_of_strings:
                linewidth = '1pt'
            else:
                linewidth = '.5pt'
            point0 = Vector2D(0, i)
            point1 = Vector2D(self.x_last_fret, i)
            self.line(point0, point1, linewidth=linewidth)

        # Paint frets
        for i in self.nut_fret_iter:
            x = self.fret_position(i)
            point0 = Vector2D(x, 0)
            point1 = Vector2D(x, self.number_of_strings)
            if i == 0:
                linewidth = '4pt'
            else:
                linewidth = '1pt'
            self.line(point0, point1, linewidth=linewidth)

        # Paint fret numbers
        for i in self.fret_iter:
            x_middle = self.middle_position(i)
            point = Vector2D(x_middle, -.25)
            self.text(point, i, anchor='north')

        # Paint pitches
        for i in self.string_iter:
            y = i
            y_middle = y + .5
            string = self.string(i)
            # string pitch
            point = Vector2D(-1, y_middle)
            self.text(point, i+1, anchor='east')
            point = Coordinate('-10em', y_middle)
            pitch = string.pitch
            english_pitch = pitch.unicode_name_with_octave
            latin_pitch = pitch.latin_unicode_name_with_octave
            self.text(point, '{} / {} / {}'.format(english_pitch, latin_pitch, int(pitch)), anchor='west')
            # fret pitches
            for i in self.fret_iter:
                fret_pitch = string[i]
                x = self.middle_position(i)
                point = Coordinate(x, y_middle)
                english_pitch = fret_pitch.unicode_name_with_octave
                latin_pitch = fret_pitch.latin_unicode_name
                self.text(point, '{} / {} / {}'.format(english_pitch, latin_pitch, int(fret_pitch)))
