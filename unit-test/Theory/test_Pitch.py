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

        self._test_pitch_parser('A',       ('A', None, None))
        self._test_pitch_parser('A#',      ('A',  1,   None))
        self._test_pitch_parser('A#4',     ('A',  1,      4))
        self._test_pitch_parser('a#4',     ('A',  1,      4))
        self._test_pitch_parser('A-##--4', ('A', -1,      4))

    ##############################################

    # @unittest.skip('')
    def test_pitch(self):

        pitch = Pitch('C4')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, 4)
        self.assertEqual(float(pitch), 60)

        pitch = Pitch('C/-1')
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, -1)
        self.assertEqual(float(pitch), 0)

        pitch = Pitch('C', octave=-1)
        self.assertEqual(pitch.step, 'C')
        self.assertEqual(pitch.octave, -1)
        self.assertEqual(float(pitch), 0)
        self.assertEqual(pitch.full_name, 'C/-1')

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

    ##############################################

    # @unittest.skip('')
    def test_midi(self):

        self.assertEqual(Pitch(midi= 60), Pitch('C4')) # Midi specification
        self.assertEqual(Pitch(midi=  0), Pitch('C', octave=-1))
        self.assertEqual(Pitch(midi= 12), Pitch('C0'))
        self.assertEqual(Pitch(midi=127), Pitch('G9'))

    ##############################################

    # @unittest.skip('')
    def test_frequency(self):

        pitch = Pitch('A4')
        self.assertAlmostEqual(pitch.frequency, 440)

    ##############################################

    # @unittest.skip('')
    def test_iterator(self):

        pitches_4 = [
            'C4',  'C#4',
            'D4',  'D#4',
            'E4',
            'F4',  'F#4',
            'G4',  'G#4',
            'A4',  'A#4',
            'B4',
        ]

        natural_pitches_4 = [
            'C4',
            'D4',
            'E4',
            'F4',
            'G4',
            'A4',
            'B4',
        ]

        pitches_3 = [pitch.replace('4', '3') for pitch in pitches_4]
        natural_pitches_3 = [pitch.replace('4', '3') for pitch in natural_pitches_4]

        pitches_5 = [pitch.replace('4', '5') for pitch in pitches_4]
        natural_pitches_5 = [pitch.replace('4', '5') for pitch in natural_pitches_4]

        pitches = pitches_3 + pitches_4 + pitches_5
        natural_pitches = natural_pitches_3 + natural_pitches_4 + natural_pitches_5
        for i in range(1, len(pitches) -1):
            prev_pitch, pitch, next_pitch = pitches[i-1], pitches[i], pitches[i+1]
            self.assertEqual(Pitch(pitch).prev_pitch(), Pitch(prev_pitch))
            self.assertEqual(Pitch(pitch).next_pitch(), Pitch(next_pitch))

        first_pitch = Pitch('C4')
        last_pitch = Pitch('C5')
        pitches = pitches_4 + [pitches_5[0]]
        natural_pitches = natural_pitches_4 + [natural_pitches_5[0]]
        for pitch, pitch_name in zip(first_pitch.pitch_iterator(last_pitch).iter(), pitches):
            self.assertEqual(pitch.full_name, pitch_name)
        for pitch, pitch_name in zip(first_pitch.pitch_iterator(last_pitch).iter(natural=True),
                                     natural_pitches
                                     ):
            self.assertEqual(pitch.full_name, pitch_name)

        first_pitch = Pitch('C5')
        for pitch, pitch_name in zip(first_pitch.pitch_iterator().iter(reverse=True),
                                     reversed(pitches)):
            self.assertEqual(pitch.full_name, pitch_name)
        for pitch, pitch_name in zip(first_pitch.pitch_iterator().iter(reverse=True, natural=True),
                                     reversed(natural_pitches)):
            self.assertEqual(pitch.full_name, pitch_name)

    ##############################################

    # @unittest.skip('')
    def test_enharmonic(self):

        self.assertTrue(Pitch('D-4').is_enharmonic(Pitch('C#4')))
        self.assertFalse(Pitch('C4').is_enharmonic(Pitch('C#4')))
        self.assertFalse(Pitch('D4').is_enharmonic(Pitch('D-4')))
        self.assertFalse(Pitch('C4#').is_enharmonic(Pitch('C#4')))
        self.assertFalse(Pitch('D-4').is_enharmonic(Pitch('D-4')))

        for pitch1, pitch2 in (
                ('C#4', 'D-4'),
                ('D#4', 'E-4'),
                ('F#4', 'G-4'),
                ('G#4', 'A-4'),
                ('A#4', 'B-4'),
        ):
            self.assertEqual(Pitch(pitch1).get_enharmonic(), Pitch(pitch2))
            self.assertEqual(Pitch(pitch2).get_enharmonic(), Pitch(pitch1))

        # getEnharmonic(E##) => F# getEnharmonic(F#) => G- getEnharmonic(A–) => G getEnharmonic(G) => F##

        #! self.assertEqual(Pitch('E##4').get_enharmonic(), Pitch('F#4'))
        self.assertEqual(Pitch('E##4').get_enharmonic(), Pitch('G-4'))
        self.assertEqual(Pitch('F#4').get_enharmonic(), Pitch('G-4'))
        #! self.assertEqual(Pitch('A--4').get_enharmonic(), Pitch('G4'))
        #! self.assertEqual(Pitch('G4').get_enharmonic(), Pitch('F##4'))

        # C <-> B#, D <-> C##, E <-> F-; F <-> E#, G <-> F##, A <-> B–, B <-> C-

    ##############################################

    # @unittest.skip('')
    def test_simplification(self):

        for pitch, alteration in (
                ('A--4', -2),
                ('A-4' , -1),
                ('A4'  ,  0),
                ('A#4' ,  1),
                ('A##4',  2),
        ):
            self.assertEqual(Pitch(pitch).alteration, alteration)

        for pitch1, pitch2 in (
                ('C##4',   'D4'),
                ('C###4',  'D#4'),
                ('C####4', 'E4'),
                ('B#4',    'C5'),
                ('B##4',   'C#5'),
                ('B###4',  'D5'),
                ('C-4',    'B3'),
                ('C--4',   'A#3'),
                ('C---4',  'A3'),
                #! ('B-4',    'A#4'),
                ('B--4',    'A4'),
                ('B---4',   'G#4'),
                ('B----4',  'G4'),
                ('C' + '#'*12 + '4', 'C5'),
                ('G' + '#'*12 + '4', 'G5'),
                ('C' + '-'*12 + '4', 'C3'),
                ('G' + '-'*12 + '4', 'G3'),
        ):
            self.assertEqual(Pitch(pitch1).simplify_accidental(), Pitch(pitch2))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
