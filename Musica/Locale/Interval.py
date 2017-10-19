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

class Interval

    ##############################################

    def __init__(self, name):

        self._name = name

####################################################################################################

class Intervals:

    __perfect__ = ('unison', 'fourth', 'fifth', 'octave')

    __intervals__ = (
        Interval(
            degree=1,
            name=_('unison'), # prime unison
            quality=_('perfect'),
        ),
        Interval(
            degree=2,
            name=_('second'), # seconde
            quality=_('minor', 'major'),
        ),
        ),
        Interval(
            degree=3,
            name=_('third'), # tierce
            quality=_('perfect'),
        ),
        Interval(
            degree=4,
            name=_('fourth'), # quarte
            quality=_('perfect'),
        ),
        Interval(
            degree=5,
            name=_('fifth'), # quinte
            quality=_('perfect'),
        Interval(
            degree=6,
            name=_('sixth'), # sixte
        Interval(
            degree=7,
            name=_('seventh'), # septième
        Interval(
            degree=8,
            name=_('octave'),
            quality=_('perfect'),
    )

    __intervals__ = (
        Interval(
            number_of_semitones=0,
            name=_('perfect unison'), # prime unison
            short=_('P1'),
            altered_name=_('diminished second'),
            altered_short=_('d2'),
            '1:1',
        ),
        Interval(
            number_of_semitones=1,
            name=_('minor second'), # seconde
            short=_('m2'),
            altered_name=_('augmented unison'),
            altered_short=_('A1'),
            alternative_names=(_('semitone'), _('half tone'), _('half step')),
            alternative_short=_('S'),
            '16:15',
        ),
        Interval(
            number_of_semitones=2,
            name=_('major second'),
            short=_('M2'),
            altered_name=_('diminished third'),
            altered_short=_('d3'),
            alternative_names=(_('tone'), _('whole tone'), _('whole step')),
            alternative_short=_('S'),
            '9:8',
        ),
        Interval(
            number_of_semitones=3,
            name=_('minor third'), # tierce
            short=_('m3'),
            altered_name=_('augmented second'),
            altered_short=_('A2'),
            '6:5',
        ),
        Interval(
            number_of_semitones=4,
            name=_('major third'),
            short=_('M3'),
            altered_name=_('diminished fourth'),
            altered_short=_('d4'),
            '5:4',
        ),
        Interval(
            number_of_semitones=5,
            name=_('perfect fourth'), # quarte
            short=_('P4'),
            altered_name=_('augmented third'),
            altered_short=_('A3'),
            '4:3',
        ),
        Interval(
            number_of_semitones=6,
            name=None,
            short=None,
            altered_name=(_('diminished fifth'), _('augmented fourth')),
            altered_short=(_('d5'), _('A4')),
            alternative_names=_('tritone'),
            alternative_short=_('TT'),
            ''),
        Interval(
            number_of_semitones=7,
            name=_('perfect fifth'), # quinte
            short=_('P5'),
            altered_name=_('diminished sixth'),
            altered_short=_('d6'),
            '3:2'),
        Interval(
            number_of_semitones=8,
            name=_('minor sixth'), # sixte
            short=_('m6'),
            altered_name=_('augmented fifth'),
            altered_short=_('A5'),
            '8:5'),
        Interval(
            number_of_semitones=9,
            name=_('major sixth'),
            short=_('M6'),
            altered_name=_('diminished seventh'),
            altered_short=_('d7'),
            '5:3'),
        Interval(
            number_of_semitones=10,
            name=_('minor seventh'), # septième
            short=_('m7'),
            altered_name=_('augmented sixth'),
            altered_short=_('A6'),
            '16:9'),
        Interval(
            number_of_semitones=11,
            name=_('major seventh'),
            short=_('M7'),
            altered_name=_('diminished octave'),
            altered_short=_('d8'),
            '15:8'),
        Interval(
            number_of_semitones=12,
            name=_('perfect octave'),
            short=_('P8'),
            altered_name=_('augmented seventh'),
            altered_short=_('A7'),
            '2:1'),
    )

####################################################################################################

# The number of an interval is the number of letter names it encompasses or staff positions it
# encompasses. Both lines and spaces are counted, including the positions of both notes forming the
# interval.

# Quality: perfect (P), major (M), minor (m), augmented (A), and diminished (d)
