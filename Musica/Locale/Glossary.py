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
    'GENERAL'
    'INTERVAL_NAMES',
    'ACCIDENTAL_NAMES'
    'OCTAVE_NAMES',
    'SCALE_DEGREES',
    ]

####################################################################################################

from . import gettext as _

####################################################################################################

GENERAL = (
    _('pitch'),
)

INTERVAL_NAMES = (
    _('semitone'), # half step or a half tone
    _('tone'),
    _('tritone'),

    _('minor'),
    _('major'),
    _('diminished'),
    _('augmented'),

    _('unison'),

    _('second'),
    _('minor second'),
    _('major second'),

    _('third'),
    _('minor third'),
    _('major third'),

    _('fourth'),
    _('perfect fourth'),

    _('fifth'),
    _('perfect fifth'),

    _('sixth'),
    _('minor sixth'),
    _('major sixth'),

    _('seventh'),
    _('minor seventh'),
    _('major seventh'),

    _('octave'),
)

ACCIDENTAL_NAMES = (
    _('double-flat'),
    _('flat'), # ♭
    _('natural'), # ♮
    _('sharp'), # ♯
    _('double-sharp'),
)

OCTAVE_NAMES = (
    _('octocontra'), # C-2
    _('subsubcontra'), # C-1
    _('subcontra'), # C0
    _('contra'), # C1
    _('great'),
    _('small'),
    _('one-lined'),
    _('two-lined'),
    _('three-lined'),
    _('four-lined'),
    _('five-lined'),
    _('six-lined'),
    _('seven-lined'), # C10
)

SCALE_DEGREES = (
    _('tonic'),        # 1
    _('supertonic'),   # 2
    _('mediant'),      # 3
    _('subdominant'),  # 4
    _('dominant'),     # 5
    _('submediant'),   # 6
    _('leading tone'), # 7
)
