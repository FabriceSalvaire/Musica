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
    'to_unicode',
    ]

####################################################################################################

# from . import gettext as _

####################################################################################################

# Note: use chr for emacs rendering issue
__map__ = {
    # Accidentals
    'double-flat': chr(0x1D12B), # U+1D12B &#119082;
    'flat': '♭', # U+266D &#9837;
    'natural': '♮', # U+266E &#9838;
    'sharp':  '♯', # U+266F &#9839;
    'double-sharp': chr(0x1D12A), # U+1D12A &#119082;

    # '####', chr(0x1d12a) + chr(0x1d12a),
    # '###', '\u266f' + chr(0x1d12a),
    # '##', chr(0x1d12a), # note that this must be expressed as a surrogate pair
    # '#~', '\u266f' + chr(0x1d132), # 1D132
    # '~', chr(0x1d132)
    # '----', chr(0x1d12b) + chr(0x1d12b),
    # '---', '\u266D',
    # '-`', '\u266D' + chr(0x1d132),
    # '`', chr(0x1d132), # 1D132 # raised flat: 1D12C
}

####################################################################################################

def to_unicode(name):
    return __map__.get(name, name)
