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
#
# Tone     T W whole
# Semitone S h half
#
# 12-tet / Gamme tempérée
#   12 pitches
#
# Major
#     T  T  S  T  T  T  S
#     W  W  H  W  W  W  H
#     2M 3M 4P 5P 6M 7M 8v
#        third is major
# Minor Harmonique
#     T  S  T  T  S  1.5T  S
#     note sensible : 1/2 ton sous la tonique
# Minor Melodic
#    T  S  T  T  T  T  S
#      third is minor
# Natural Minor Scale / Mode Aeolian / Éolien
#    T  S  T  T  S  T  T
#
# 7-pitch scale
# Natural Minor Scale | T  S T  T  S T  T  |
# Minor Harmonique    | T  S T  T  S 3   S |
# Minor Melodic       | T  S T  T  T  T  S |
# Major               | T  T  S T  T  T  S |
#
# 5-pitch scale
# Pentatonic Minor | 3   T  T  3   T  |
# Pentatonic Major | T  T  3   T  3   | Minor << 1
#
# |     | Mode       |            | Also known as       | Tonic relative | Specific | Interval      |
# |     |            |            |                     | to major scale | Pitch    | sequence      |
# | Do  | Ionian     | Ionien     | Major scale         | I              | Ref.     | T T S T T T S |
# | Ré  | Dorian     | Dorien     |                     | II             | 6M       | T S T T T S T | Major << 1
# | Mi  | Phrygian   | Phrygien   |                     | III            | 2m       | S T T T S T T | Major << 2
# | Fa  | Lydian     | Lydien     |                     | IV             | 4aug     | T T T S T T S | Major << 3
# | Sol | Mixolydian | Mixolydien | "Dominant scale"    | V              | 7m       | T T S T T S T | Major << 4
# | La  | Aeolian    | Éoloien    | Natural minor scale | VI             | Ref.     | T S T T S T T | Major << 5 / Major >> 2
# | Si  | Locrian    | Lociren    |                     | VII            | 2m 5dim  | S T T S T T T | Major << 6
#
# Major/Ionan Scale
#   It is made up of seven distinct notes, plus an eighth that duplicates the first an octave higher.
#
#   A major scale may be seen as two identical tetrachords separated by a whole tone. Each
#   tetrachord consists of two whole tones followed by a semitone: whole, whole, half.
#
#
####################################################################################################
