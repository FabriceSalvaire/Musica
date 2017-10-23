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

from Musica.Math.MusicTheory import *

####################################################################################################

class TestMusicTheory(unittest.TestCase):

    ##############################################

    # @unittest.skip('')
    def test(self):

        frequency = Frequency(50)
        self.assertEqual(frequency.period, 1/50)

        A440 = Frequency(440)
        A880 = Frequency(2 * float(A440))

        self.assertEqual(float(A440 / A440), 0)
        self.assertEqual(float(A880 / A440), 1200)

        self.assertEqual((A880 / A440).to_frequency(A440), A880)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
