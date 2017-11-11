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

from IntervalArithmetic import IntervalInt

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

    # alias
    first_pitch = pitch

    @property
    def last_pitch(self):
        return self._pitches[-1]

    @property
    def pitch_interval(self):
        # /!\ midi note, i.e. int not float
        return IntervalInt(int(self.first_pitch), int(self.last_pitch))

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

class PitchInterval:

    ##############################################

    @classmethod
    def make_C_E_interval(cls, octave):

        lower_pitch = Pitch('C', octave=octave)
        upper_pitch = Pitch('E', octave=octave)

        return cls(lower_pitch, upper_pitch)

    ##############################################

    @classmethod
    def make_F_B_interval(cls, octave):

        lower_pitch = Pitch('F', octave=octave)
        upper_pitch = Pitch('B', octave=octave)

        return cls(lower_pitch, upper_pitch)

    ##############################################

    def __init__(self, lower_pitch, upper_pitch):

        self._lower_pitch = lower_pitch
        self._upper_pitch = upper_pitch
        self._interval = IntervalInt(int(lower_pitch), int(upper_pitch))

    ##############################################

    @property
    def lower_pitch(self):
        return self._lower_pitch

    @property
    def upper_pitch(self):
        return self._upper_pitch

    @property
    def interval(self):
        return self._interval

    ##############################################

    def __len__(self):
        return self._interval.length

    ##############################################

    def __repr__(self):
        return '{0._lower_pitch} {0._upper_pitch}'.format(self)

    ##############################################

    def __contains__(self, pitch):
        return int(pitch) in self._interval

    ##############################################

    def length_from(self, pitch):

        if pitch in self:
            delta = int(pitch) - self._interval.inf
            print(pitch, self._interval.length, delta)
            return self._interval.length - delta
        else:
            raise ValueError("Invalid pitch {} for {}".format(pitch, self))

####################################################################################################

class PitchIntervals:

    ##############################################

    def __init__(self, lower_pitch, upper_pitch):

        # Split in block (C, D, E) (F, G, A, B)
        self._pitch_intervals = []

        octave = lower_pitch.octave
        if lower_pitch.degree < 3:
            pitch_interval = PitchInterval.make_C_E_interval(octave)
            is_C_E = True
        else:
            pitch_interval = PitchInterval.make_F_B_interval(octave)
            octave += 1
            is_C_E = False
        self._pitch_intervals.append(pitch_interval)

        while pitch_interval.upper_pitch < upper_pitch:
            if is_C_E:
                pitch_interval = PitchInterval.make_F_B_interval(octave)
                octave += 1
            else:
                pitch_interval = PitchInterval.make_C_E_interval(octave)
            is_C_E = not is_C_E
            self._pitch_intervals.append(pitch_interval)

    ##############################################

    def __len__(self):
        return len(self._pitch_intervals)

    ##############################################

    def __iter__(self):
        return iter(self._pitch_intervals)

    ##############################################

    def matchings_interval(self, lower_pitch, upper_pitch):

        # Faster algo: compute delta ???

        pitch_intervals = []
        start = True
        for interval in self._pitch_intervals:
            if start:
                if lower_pitch in interval:
                    pitch_intervals.append(interval)
                    start = False
            else:
                pitch_intervals.append(interval)
            if upper_pitch in interval:
                break

        return pitch_intervals

####################################################################################################

class FretboardFigure(TikzFigure, Fretboard):

    ##############################################

    def __init__(self, **kwargs):

        Fretboard.__init__(self, **kwargs)

        # for i in self.string_iter:
        #     string1_interval = self.string(i).pitch_interval
        #     for j in self.string_iter:
        #         if j != i:
        #             string2_interval = self.string(j).pitch_interval
        #             if string1_interval.intersect(string2_interval):
        #                 intersection = string1_interval & string2_interval
        #                 print(i, j, string1_interval, string2_interval, '&', intersection, 'P', ' '.join([str(x) for x in new_parts]))

        fretboard_interval = None
        for string in self.string_fretboard_iter:
            if fretboard_interval is None:
                fretboard_interval = string.pitch_interval.clone()
            else:
                fretboard_interval |= string.pitch_interval
        lower_pitch = Pitch(midi=fretboard_interval.inf)
        upper_pitch = Pitch(midi=fretboard_interval.sup)
        pitch_intervals = PitchIntervals(lower_pitch, upper_pitch)

        # Fixme: scale, paper
        TikzFigure.__init__(self, options='x=.5mm,y=5mm')

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(4)

        # Fixme: broken corner

        # Mark
        #   circle: 3, 5, 7, 9, 15, 17
        #   2 circles: 12

        delta_hue = 360 / len(pitch_intervals)
        hue = delta_hue
        even = True
        for i, pitch_interval in enumerate(pitch_intervals):
            name = 'color{}'.format(i)
            if even:
                hue = (i+1) * delta_hue
            else:
                hue = (i-1) * delta_hue
            hue = hue % 360
            self.append(self.format(r'\definecolor{«»}{Hsb}{«»,0.3,1}', name, hue))
            pitch_interval.colour = name
            even = not even

        # Paint pitch intervals
        for i, string in enumerate(self.string_fretboard_iter):
            y = i
            string_pitch_intervals = pitch_intervals.matchings_interval(string.first_pitch, string.last_pitch)
            lower_fret = 0
            for interval in string_pitch_intervals:
                interval_length = interval.length_from(string[lower_fret])
                upper_fret = min(lower_fret + interval_length -1, self.number_of_frets)
                if lower_fret:
                    lower_x = self.fret_position(lower_fret-1)
                else:
                    lower_x = '-10em'
                # print(i, interval, interval_length, lower_fret, upper_fret)
                upper_x = self.fret_position(upper_fret)
                point0 = Coordinate(lower_x, y)
                point1 = Coordinate(upper_x, y+1)
                self.rectangle(point0, point1, fill=interval.colour)
                lower_fret = upper_fret +1

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
            point = Coordinate('-7em', y_middle)
            self.text(point, i+1, anchor='east')
            point = Coordinate('-1em', y_middle)
            pitch = string.pitch
            english_pitch = pitch.unicode_name_with_octave
            latin_pitch = pitch.latin_unicode_name_with_octave
            self.text(point, '{} / {}'.format(english_pitch, latin_pitch), anchor='east')
            # fret pitches
            for i in self.fret_iter:
                fret_pitch = string[i]
                x = self.middle_position(i)
                point = Coordinate(x, y_middle)
                english_pitch = fret_pitch.unicode_name_with_octave
                latin_pitch = fret_pitch.latin_unicode_name
                self.text(point, '{} / {}'.format(english_pitch, latin_pitch))

        # Paint decorations
        for i in (5, 7, 9): # 12 15 17
            x = self.middle_position(i)
            point = Coordinate(x, self.number_of_strings / 2)
            self.circle(point, radius='1mm', fill=True)
        x = self.fret_position(12)
        for y in (-1, 1):
            point = Coordinate(x, (.5 + y * .1) *  self.number_of_strings)
            self.circle(point, radius='1mm', fill=True)
