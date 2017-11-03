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
        if accidental is not None:
            self.assertTupleEqual((step, accidental.alteration, octave), answer)
        else:
            self.assertTupleEqual((step, None, octave), answer)

    ##############################################

    # @unittest.skip('')
    def test_pitch_parser(self):

        self._test_pitch_parser('A', ('A', None, None))
        self._test_pitch_parser('A#', ('A', 1, None))
        self._test_pitch_parser('A#4', ('A', 1, 4))
        self._test_pitch_parser('a#4', ('A', 1, 4))
        self._test_pitch_parser('A-##--4', ('A', -1, 4))

    ##############################################

    # @unittest.skip('')
    def test_pitch(self):

        pitch = Pitch('C4')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, 4)
        self.assertEqual(float(pitch), 60)

        pitch = Pitch('C#4')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, 4)
        self.assertEqual(float(pitch), 61)

        pitch = Pitch(step='C')
        self.assertEqual(pitch.step, 'C')
        self.assertIsNone(pitch.accidental)
        self.assertIsNone(pitch.octave)

        pitch = Pitch(step='C', accidental='#', octave=4)
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.accidental, Accidental('#'))
        self.assertEqual(pitch.octave, 4)

        step_name_to_number = {
            'C' : 0,
            'D' : 2,
            'E' : 4,
            'F' : 5,
            'G' : 7,
            'A' : 9,
            'B' : 11,
        }

        for name, number in step_name_to_number.items():
            pitch = Pitch(number)
            self.assertEqual(pitch.step, name)
            self.assertIsNone(pitch.accidental)
            self.assertIsNone(pitch.octave)
            self.assertFalse(pitch.spelling_is_inferred)

        pitch = Pitch(1)
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.accidental, Accidental('#'))
        self.assertIsNone(pitch.octave)
        self.assertTrue(pitch.spelling_is_inferred)

        self.assertEqual(float(Pitch('D4')), 62)
        self.assertEqual(float(Pitch('B###3')), 62)

        pitch = Pitch('C')
        self.assertEqual(str(pitch), 'C')

        pitch = Pitch('C-')
        self.assertEqual(str(pitch), 'C-')

        pitch = Pitch('C#')
        self.assertEqual(str(pitch), 'C#')

        pitch = Pitch('C4')
        self.assertEqual(str(pitch), 'C4')

        pitch = Pitch('C#4')
        self.assertEqual(str(pitch), 'C#4')
        # print(pitch.unicode_name)

        pitch = Pitch('A4')
        self.assertAlmostEqual(pitch.frequency, 440)

        first_pitch = Pitch('C4')
        last_pitch = Pitch('C5')
        for pitch, pitch_name in zip(first_pitch.pitch_iterator(last_pitch),
                                     ('C4', 'C#4',
                                      'D4', 'D#4',
                                      'E4',
                                      'F4', 'F#4',
                                      'G4', 'G#4',
                                      'A4', 'A#4',
                                      'B4',
                                      'C5')):
            self.assertEqual(pitch.full_name, pitch_name)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
