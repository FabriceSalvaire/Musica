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

from Musica.Notation.Stave import *
from Musica.Theory.Pitch import *

####################################################################################################

class TestStave(unittest.TestCase):

    ##############################################

    # @unittest.skip('')
    def test(self):

        treble_clef = TrebleKey()
        stave = Stave(treble_clef)
        reference_line = treble_clef.line
        pitch_iterator = Pitch(treble_clef.pitch).pitch_iterator()
        for reverse in (True, False):
            direction = -1 if reverse else 1
            for i, pitch in enumerate(pitch_iterator.iter(natural=True, reverse=reverse)):
                if i > 15: # 3 staves
                    break
                line = reference_line + direction * i / 2
                print(line, pitch)
                self.assertEqual(stave.line_to_pitch(line), pitch)
                self.assertEqual(stave.pitch_to_line(pitch), line)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
