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

from Musica.Theory.Pitch import *

####################################################################################################

class TestPitch(unittest.TestCase):

    ##############################################

    def _test_pitch_parser(self, name, answer):

        step, accidental, octave = Pitch.parse_pitch(name)
        self.assertTupleEqual((step, accidental.accidental, octave), answer)

    ##############################################

    # @unittest.skip('')
    def test_et12(self):

        self.assertAlmostEqual(ET12.fundamental, 32.70, 2)
        self.assertAlmostEqual(ET12.frequency(octave_number=4, interval_number=10), 440)
        self.assertAlmostEqual(ET12.frequency(octave_number=8, interval_number=12), 7902.13, 2)

        self.assertEqual(Accidental.reduce_accidental(''), 0)
        self.assertEqual(Accidental.reduce_accidental('#'), 1)
        self.assertEqual(Accidental.reduce_accidental('###'), 3)
        self.assertEqual(Accidental.reduce_accidental('-'), -1)
        self.assertEqual(Accidental.reduce_accidental('---'), -3)
        self.assertEqual(Accidental.reduce_accidental('-#-'), -1)
        self.assertEqual(Accidental.reduce_accidental('-##-'), 0)

        self._test_pitch_parser('A', ('A', 0, None))
        self._test_pitch_parser('A#', ('A', 1, None))
        self._test_pitch_parser('A#4', ('A', 1, 4))
        self._test_pitch_parser('a#4', ('A', 1, 4))
        self._test_pitch_parser('A-##--4', ('A', -1, 4))

        pitch = Pitch('C4')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, 4)
        self.assertEqual(float(pitch), 60)

        pitch = Pitch('C#4')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, 4)
        self.assertEqual(float(pitch), 61)

        self.assertEqual(float(Pitch('D4')), 62)
        self.assertEqual(float(Pitch('B###3')), 62)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
