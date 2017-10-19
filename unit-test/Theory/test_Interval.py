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

import unittest

####################################################################################################

from Musica.Theory.Pitch import Pitch
from Musica.Theory.Interval import *

####################################################################################################

class TestInterval(unittest.TestCase):

    ##############################################

    def test(self):

        interval = Interval(Pitch('A-'), Pitch('B#'))
        interval = Interval(Pitch('A'),  Pitch('C#'))
        interval = Interval(Pitch('A'),  Pitch('D-'))
        interval = Interval(Pitch('A#'), Pitch('E--'))

        interval = Interval(Pitch('F#'), Pitch('A#'))
        interval = Interval(Pitch('G-'), Pitch('B-'))
        interval = Interval(Pitch('F#'), Pitch('B-'))
        interval = Interval(Pitch('G-'), Pitch('A#'))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
