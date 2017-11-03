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

from Musica.Theory.Temperament import *

####################################################################################################

class TestTemperament(unittest.TestCase):

    ##############################################

    # @unittest.skip('')
    def test_et12(self):

        self.assertAlmostEqual(ET12.fundamental, 16.352, 3)
        self.assertAlmostEqual(ET12.frequency(octave=4, step_number=9), 440)
        self.assertAlmostEqual(ET12.frequency(octave=8, step_number=11), 7902.13, 2)

####################################################################################################

if __name__ == '__main__':

    unittest.main()
