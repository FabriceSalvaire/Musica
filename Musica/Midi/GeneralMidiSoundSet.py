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

"""General Midi 1 Sound Set

Reference links:

* https://www.midi.org/specifications/category/gm-specifications
* https://www.midi.org/specifications/item/gm-level-1-sound-set

"""

# General MIDI's most recognized feature is the defined list of sounds (or "patches"). However,
# General MIDI does not actually define the way the sound will be reproduced, only the name of that
# sound. Though this can obviously result in wide variations in performance from the same song data
# on different GM sound sources, the authors of General MIDI felt it important to allow each
# manufacturer to have their own ideas and express their personal aesthetics when it comes to
# picking the exact timbres for each sound.
#
# Each manufacturer must insure that their sounds provide an acceptable representation of song data
# written for General MIDI. Guidelines for developing GM compatible sound sets and song data are
# available.
#
#    The names of the instruments indicate what sort of sound will be heard when that instrument
#    number (MIDI Program Change or "PC#") is selected on the GM1 synthesizer.
#
#    These sounds are the same for all MIDI Channels except Channel 10, which has only "percussion"
#    sounds.

####################################################################################################

__all__ = [
    ]

####################################################################################################

# General MIDI Level 1 Instrument Families
#
# The General MIDI Level 1 instrument sounds are grouped by families. In each family are 8 specific
# instruments.

InstrumentFamilies = (
    # PC, Family Name
    (  1,   8, 'Piano'),
    (  9,  16, 'Chromatic Percussion'),
    ( 17,  24, 'Organ'),
    ( 25,  32, 'Guitar'),
    ( 33,  40, 'Bass'),
    ( 41,  48, 'Strings'),
    ( 49,  56, 'Ensemble'),
    ( 57,  64, 'Brass'),
    ( 65,  72, 'Reed'),
    ( 73,  80, 'Pipe'),
    ( 81,  88, 'Synth Lead'),
    ( 89,  96, 'Synth Pad'),
    ( 97, 104, 'Synth Effects'),
    (105, 112, 'Ethnic'),
    (113, 120, 'Percussive'),
    (121, 128, 'Sound Effects'),
)

####################################################################################################

# General MIDI Level 1 Instrument Patch Map
#
# Note: While GM1 does not define the actual characteristics of any sounds, the names in parentheses
# after each of the synth leads, pads, and sound effects are, in particular, intended only as
# guides).

InstrumentMap = (
    # PC, Instrument Name
    1:   'Acoustic Grand Piano',
    2:   'Bright Acoustic Piano',
    3:   'Electric Grand Piano',
    4:   'Honky-tonk Piano',
    5:   'Electric Piano 1',
    6:   'Electric Piano 2',
    7:   'Harpsichord',
    8:   'Clavi',
    9:   'Celesta',
    10:  'Glockenspiel',
    11:  'Music Box',
    12:  'Vibraphone',
    13:  'Marimba',
    14:  'Xylophone',
    15:  'Tubular Bells',
    16:  'Dulcimer',
    17:  'Drawbar Organ',
    18:  'Percussive Organ',
    19:  'Rock Organ',
    20:  'Church Organ',
    21:  'Reed Organ',
    22:  'Accordion',
    23:  'Harmonica',
    24:  'Tango Accordion',
    25:  'Acoustic Guitar (nylon)',
    26:  'Acoustic Guitar (steel)',
    27:  'Electric Guitar (jazz)',
    28:  'Electric Guitar (clean)',
    29:  'Electric Guitar (muted)',
    30:  'Overdriven Guitar',
    31:  'Distortion Guitar',
    32:  'Guitar harmonics',
    33:  'Acoustic Bass',
    34:  'Electric Bass (finger)',
    35:  'Electric Bass (pick)',
    36:  'Fretless Bass',
    37:  'Slap Bass 1',
    38:  'Slap Bass 2',
    39:  'Synth Bass 1',
    40:  'Synth Bass 2',
    41:  'Violin',
    42:  'Viola',
    43:  'Cello',
    44:  'Contrabass',
    45:  'Tremolo Strings',
    46:  'Pizzicato Strings',
    47:  'Orchestral Harp',
    48:  'Timpani',
    49:  'String Ensemble 1',
    50:  'String Ensemble 2',
    51:  'SynthStrings 1',
    52:  'SynthStrings 2',
    53:  'Choir Aahs',
    54:  'Voice Oohs',
    55:  'Synth Voice',
    56:  'Orchestra Hit',
    57:  'Trumpet',
    58:  'Trombone',
    59:  'Tuba',
    60:  'Muted Trumpet',
    61:  'French Horn',
    62:  'Brass Section',
    63:  'SynthBrass 1',
    64:  'SynthBrass 2',
    65:  'Soprano Sax',
    66:  'Alto Sax',
    67:  'Tenor Sax',
    68:  'Baritone Sax',
    69:  'Oboe',
    70:  'English Horn',
    71:  'Bassoon',
    72:  'Clarinet',
    73:  'Piccolo',
    74:  'Flute',
    75:  'Recorder',
    76:  'Pan Flute',
    77:  'Blown Bottle',
    78:  'Shakuhachi',
    79:  'Whistle',
    80:  'Ocarina',
    81:  'Lead 1 (square)',
    82:  'Lead 2 (sawtooth)',
    83:  'Lead 3 (calliope)',
    84:  'Lead 4 (chiff)',
    85:  'Lead 5 (charang)',
    86:  'Lead 6 (voice)',
    87:  'Lead 7 (fifths)',
    88:  'Lead 8 (bass + lead)',
    89:  'Pad 1 (new age)',
    90:  'Pad 2 (warm)',
    91:  'Pad 3 (polysynth)',
    92:  'Pad 4 (choir)',
    93:  'Pad 5 (bowed)',
    94:  'Pad 6 (metallic)',
    95:  'Pad 7 (halo)',
    96:  'Pad 8 (sweep)',
    97:  'FX 1 (rain)',
    98:  'FX 2 (soundtrack)',
    99:  'FX 3 (crystal)',
    100: 'FX 4 (atmosphere)',
    101: 'FX 5 (brightness)',
    102: 'FX 6 (goblins)',
    103: 'FX 7 (echoes)',
    104: 'FX 8 (sci-fi)',
    105: 'Sitar',
    106: 'Banjo',
    107: 'Shamisen',
    108: 'Koto',
    109: 'Kalimba',
    110: 'Bag pipe',
    111: 'Fiddle',
    112: 'Shanai',
    113: 'Tinkle Bell',
    114: 'Agogo',
    115: 'Steel Drums',
    116: 'Woodblock',
    117: 'Taiko Drum',
    118: 'Melodic Tom',
    119: 'Synth Drum',
    120: 'Reverse Cymbal',
    121: 'Guitar Fret Noise',
    122: 'Breath Noise',
    123: 'Seashore',
    124: 'Bird Tweet',
    125: 'Telephone Ring',
    126: 'Helicopter',
    127: 'Applause',
    128: 'Gunshot',
)

for key, name in InstrumentMap:
    InstrumentMap[name] = key

####################################################################################################

# General MIDI Level 1 Percussion Key Map
#
# On MIDI Channel 10, each MIDI Note number ("Key#") corresponds to a different drum sound, as shown
# below. GM-compatible instruments must have the sounds on the keys shown here. While many current
# instruments also have additional sounds above or below the range show here, and may even have
# additional "kits" with variations of these sounds, only these sounds are supported by General MIDI
# Level 1 devices.

PercussionMap = {
    # 47 Percussion sounds
    # Key, Drum Sound
    35: 'Acoustic Bass Drum',
    36: 'Bass Drum 1',
    37: 'Side Stick',
    38: 'Acoustic Snare',
    39: 'Hand Clap',
    40: 'Electric Snare',
    41: 'Low Floor Tom',
    42: 'Closed Hi Hat',
    43: 'High Floor Tom',
    44: 'Pedal Hi-Hat',
    45: 'Low Tom',
    46: 'Open Hi-Hat',
    47: 'Low-Mid Tom',
    48: 'Hi-Mid Tom',
    49: 'Crash Cymbal 1',
    50: 'High Tom',
    51: 'Ride Cymbal 1',
    52: 'Chinese Cymbal',
    53: 'Ride Bell',
    54: 'Tambourine',
    55: 'Splash Cymbal',
    56: 'Cowbell',
    57: 'Crash Cymbal 2',
    58: 'Vibraslap',
    59: 'Ride Cymbal 2',
    60: 'Hi Bongo',
    61: 'Low Bongo',
    62: 'Mute Hi Conga',
    63: 'Open Hi Conga',
    64: 'Low Conga',
    65: 'High Timbale',
    66: 'Low Timbale',
    67: 'High Agogo',
    68: 'Low Agogo',
    69: 'Cabasa',
    70: 'Maracas',
    71: 'Short Whistle',
    72: 'Long Whistle',
    73: 'Short Guiro',
    74: 'Long Guiro',
    75: 'Claves',
    76: 'Hi Wood Block',
    77: 'Low Wood Block',
    78: 'Mute Cuica',
    79: 'Open Cuica',
    80: 'Mute Triangle',
    81: 'Open Triangle',
}

for key, name in PercussionMap:
    PercussionMap[name] = key
