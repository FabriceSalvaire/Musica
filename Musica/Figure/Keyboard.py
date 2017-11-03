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
    ]

####################################################################################################

import math

from ..Geometry.Path import Polyline
from ..Geometry.Transformation import AffineTransformation2D
from ..Geometry.Vector import Vector2D
from ..Tex.Tikz import TikzFigure
from ..Theory.Pitch import Pitch

####################################################################################################

class KeyboardSizing:

    # In Germany DIN 8996 (Klaviatur für Pianos und Flügel ; Maße)
    #   Yamaha is ranging from 159 to 164 mm
    # white width / largeur des marches         |    23.6 mm
    # black width / largeur des feintes         |    11.5 mm (48.7 %)
    # octave width / empan de l'octave (7 keys) |   165.2 mm (23.6 * 7)
    # keyboard width (88 keys)                  | 1 227.0 mm (+4/-0 mm)

    # Key length depend of the keyboard model
    #  typically for a grand piano, smaller keyboards have shorter keys
    # white length                              |   145.0 mm
    # black length                              |    95.0 mm (-50 mm, 65.5 %)

    __white_width__  =  23.6 # mm
    __black_width__  =  11.5
    __white_length__ = 145
    __black_length__ =  85

    ##############################################

    @classmethod
    def scale(cls, **kwargs):

        if 'octave_width' in kwargs:
            white_width = kwargs['octave_width'] / 7
        elif 'width_scale' in kwargs:
            white_width = cls.__white_length__ * kwargs['width_scale']
        else:
            white_width  = kwargs.get('white_width', cls.__white_width__)

        if 'length_scale' in kwargs:
            white_length = cls.__white_length__ * kwargs['length_scale']
        else:
            white_length  = kwargs.get('white_length', cls.__white_length__)

        # Fixme: black ...

        return cls(white_width=white_width,
                   white_length=white_length)

    ##############################################

    def __init__(self, **kwargs):

        self._white_width  = kwargs.get('white_width', self.__white_width__)
        self._black_width  = kwargs.get('black_width', self.__black_width__)
        self._white_length = kwargs.get('white_length', self.__white_length__)
        self._black_length = kwargs.get('black_length', self.__black_length__)

    ##############################################

    @property
    def white_width(self):
        return self._white_width

    @property
    def white_length(self):
        return self._white_length

    @property
    def black_width(self):
        return self._black_width

    @property
    def black_length(self):
        return self._black_length

    ##############################################

    @property
    def black_width_ratio(self):
        return self._black_width / self._white_width

    @property
    def black_length_ratio(self):
        return self._black_length / self._white_length

    ##############################################

    @property
    def octave_width(self):
        return self._white_width * 7

    ##############################################

    def keyboard_width(self, number_of_key=52):

        """A 88 key model has 52 white key and 36 black keys, spanning over 7 octaves from A0 to C8.

        """

        return self._white_width * number_of_key

####################################################################################################

class KeyGeometry:

    ##############################################

    def __init__(self, sizing):

        self._sizing = sizing
        self._path = None
        self._lower_point = None
        self._upper_point = None

    ##############################################

    @property
    def sizing(self):
        return self._sizing

    @property
    def lower_point(self):
        return self._lower_point

    @property
    def upper_point(self):
        return self._upper_point

    @property
    def path(self):
        return self._path

####################################################################################################

class BlackKeyGeometry(KeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        x_sup = self._sizing.black_width / 2
        x_inf = -x_sup

        y_sup = self._sizing.white_length
        y_inf = y_sup - self._sizing.black_length

        x_center = (x_sup + x_inf) / 2
        self._lower_point = Vector2D(x_center, 0)
        self._upper_point = Vector2D(x_center, y_sup)

        self._path = Polyline(
            (x_inf, y_inf),
            (x_inf, y_sup),
            (x_sup, y_sup),
            (x_sup, y_inf),
        )

####################################################################################################

class WhiteKeyGeometry(KeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        self._x_inf = 0
        self._x_sup = self._sizing.white_width

        self._y_inf = 0
        self._y_sup = self._sizing.white_length

        self._x_black_inf = self._sizing.black_width / 2
        self._x_black_sup = self._x_sup - self._x_black_inf
        self._y_black = self._y_sup - self._sizing.black_length

        self._lower_corner = Vector2D(self._x_inf, self._y_inf)
        self._upper_corner = Vector2D(self._x_sup, self._y_sup)

        x_center = (self._x_sup   + self._x_inf) / 2
        y_center = (self._y_black + self._y_inf) / 2
        self._lower_point = Vector2D(x_center, self._y_inf)
        self._upper_point = Vector2D(x_center, self._y_sup)
        self._center = Vector2D(x_center, y_center)

    ##############################################

    @property
    def lower_corner(self):
        return self._lower_corner

    @property
    def upper_corner(self):
        return self._upper_corner

    @property
    def center(self):
        return self._center

####################################################################################################

class WhiteLeftKeyGeometry(WhiteKeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        self._path = Polyline(
            (self._x_inf,       self._y_inf),
            (self._x_inf,       self._y_black),
            (self._x_black_inf, self._y_black),
            (self._x_black_inf, self._y_sup),
            (self._x_sup,       self._y_sup),
            (self._x_sup,       self._y_inf),
        )

####################################################################################################

class WhiteCenterKeyGeometry(WhiteKeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        self._path = Polyline(
            (self._x_inf,       self._y_inf),
            (self._x_inf,       self._y_black),
            (self._x_black_inf, self._y_black),
            (self._x_black_inf, self._y_sup),
            (self._x_black_sup, self._y_sup),
            (self._x_black_sup, self._y_black),
            (self._x_sup,       self._y_black),
            (self._x_sup,       self._y_inf),
        )

####################################################################################################

class WhiteRightKeyGeometry(WhiteKeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        self._path = Polyline(
            (self._x_inf,       self._y_inf),
            (self._x_inf,       self._y_sup),
            (self._x_black_sup, self._y_sup),
            (self._x_black_sup, self._y_black),
            (self._x_sup,       self._y_black),
            (self._x_sup,       self._y_inf),
        )

####################################################################################################

class WhiteFullKeyGeometry(WhiteKeyGeometry):

    ##############################################

    def __init__(self, sizing):

        super().__init__(sizing)

        self._path = Polyline(
            (self._x_inf,       self._y_inf),
            (self._x_inf,       self._y_sup),
            (self._x_sup,       self._y_sup),
            (self._x_sup,       self._y_inf),
        )

####################################################################################################

class Key:

    ##############################################

    def __init__(self, key_number, pitch, geometry, transformation):

        self._number = key_number
        self._pitch = pitch
        self._geometry = geometry
        self._transformation = transformation

    ##############################################

    @property
    def number(self):
        return self._number

    @property
    def pitch(self):
        return self._pitch

    @property
    def is_black(self):
        return self._pitch.is_altered

    @property
    def geometry(self):
        return self._geometry

    @property
    def transformation(self):
        return self._transformation

    @property
    def transformed_path(self):
        return self._transformation * self._geometry.path

    ##############################################

    def _transform_point(self, point):
        return Vector2D(self._transformation * point)

    ##############################################

    @property
    def lower_corner(self):
        return self._transform_point(self._geometry.lower_corner)

    @property
    def upper_corner(self):
        return self._transform_point(self._geometry.upper_corner)

    @property
    def lower_point(self):
        return self._transform_point(self._geometry.lower_point)

    @property
    def upper_point(self):
        return self._transform_point(self._geometry.upper_point)

    @property
    def center(self):
        return self._transform_point(self._geometry.center)

####################################################################################################

class KeyboardGeometry:

    ##############################################

    def __init__(self, sizing=KeyboardSizing(), first_pitch='A0', last_pitch='C8'):

        self._sizing = sizing

        self._first_pitch = first_pitch
        self._last_pitch = last_pitch

        self._black_geometry = BlackKeyGeometry(sizing)
        self._white_left_geometry = WhiteLeftKeyGeometry(sizing)
        self._white_center_geometry = WhiteCenterKeyGeometry(sizing)
        self._white_right_geometry = WhiteRightKeyGeometry(sizing)
        self._white_full_geometry = WhiteFullKeyGeometry(sizing)

        self._keys = []
        pitches = [pitch for pitch in Pitch(self._first_pitch).pitch_iterator(Pitch(self._last_pitch))]
        last_pitch_index = len(pitches) -1
        position = 0
        for i, pitch in enumerate(pitches):
            if pitch.is_altered:
                geometry = self._black_geometry
            elif i == last_pitch_index:
                geometry = self._white_full_geometry
            else:
                if i > 0:
                    prev_is_black = pitches[i-1].is_altered
                else:
                    prev_is_black = False
                if i < last_pitch_index:
                    next_is_black = pitches[i+1].is_altered
                else:
                    next_is_black = False
                if next_is_black:
                    if prev_is_black:
                        geometry = self._white_center_geometry
                    else:
                        geometry = self._white_right_geometry
                else:
                    geometry = self._white_left_geometry
            offset = Vector2D(position*self._sizing.white_width, 0)
            translation = AffineTransformation2D.Translation(offset)
            key = Key(i +1, pitch, geometry, translation)
            self._keys.append(key)
            if not pitch.is_altered:
                position += 1

    ##############################################

    @property
    def key_length(self):
        return self._sizing.white_length

    ##############################################

    def key_length_offset(self, ratio):
        return Vector2D(0, self._sizing.white_length * ratio / 100)

    ##############################################

    def __iter__(self):
        return iter(self._keys)

    ##############################################

    def __getitem__(self, slice_):
        return self._keys[slice_]

####################################################################################################

class Keyboard(TikzFigure):

    ##############################################

    def __init__(self,
                 first_pitch,
                 last_pitch,
                 style,
    ):

        super().__init__(options='x=.1mm,y=.1mm')

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(4)

        geometry = KeyboardGeometry(first_pitch=first_pitch, last_pitch=last_pitch)
        for key in geometry:
            pitch = key.pitch
            kwargs = dict(close=True)
            if key.is_black:
                kwargs['fill'] = 'black'
                kwargs['draw'] = 'black'
            else:
                kwargs['fill'] = 'white'
                kwargs['draw'] = 'black'
                for pitch_key in (pitch.full_name, pitch.step):
                    if pitch_key in style:
                        kwargs.update(style[pitch_key])
                        break
            self.path(key.transformed_path, **kwargs)
            if key.number == 44:
                self.line(key.upper_corner, key.upper_corner +  geometry.key_length_offset(20))
            if key.is_black:
                frequency_point = key.lower_point - geometry.key_length_offset(30)
            else:
                position = key.center + geometry.key_length_offset(key.pitch.degree)
                self.node(position, pitch.full_name)
                self.node(position - geometry.key_length_offset(5), pitch.french_locale.name, anchor='north')
                self.node(key.upper_point, key.number, anchor='south')
                frequency_point = key.lower_point
            frequency = int(round(pitch.frequency))
            # frequency = '{:.1f}'.format(pitch.frequency)
            self.node(frequency_point, frequency, anchor='east', rotate=90)

####################################################################################################

class FullKeyboard(Keyboard):

    ##############################################

    def __init__(self):

        super().__init__(
            first_pitch='A0',
            last_pitch='C8',
            style={
                'C4': {'fill':'red!10'},
                'A4': {'fill':'red!10'},

                'C': {'fill':'blue!10'},
                # 'D': {'fill':'red!10'},
                # 'E': {'fill':'red!10'},
                # 'F': {'fill':'red!10'},
                # 'G': {'fill':'green!10'},
                # 'A': {'fill':'green!10'},
                # 'B': {'fill':'green!10'},
            }
        )
