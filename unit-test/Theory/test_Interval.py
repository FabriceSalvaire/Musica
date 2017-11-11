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

    def _test_interval(self, note1, note2, truth):

        pitch1, pitch2 = [Pitch(note) for note in (note1, note2)]
        self.assertEqual(Interval(pitch1, pitch2).short_name, truth)

    ##############################################

    @unittest.skip('')
    def test(self):

        self._test_interval('A-', 'B#',  'AA2')
        self._test_interval('A',  'C#',  'M3')
        self._test_interval('A',  'D-',  'd4')
        self._test_interval('A#', 'E--', 'ddd5')

        self._test_interval('F#', 'A#',  'M3')
        self._test_interval('G-', 'B-',  'M3')
        self._test_interval('F#', 'B-',  'd4')
        self._test_interval('G-', 'A#',  'AA2')

####################################################################################################

if __name__ == '__main__':

    unittest.main()
