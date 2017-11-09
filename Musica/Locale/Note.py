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
    'ET12_NOTE_NAMES',
    'translate_et12_note'
    ]

####################################################################################################

# from . import gettext as _

####################################################################################################

class NoteNameTranslation:

    ##############################################

    def __init__(self, step,
                 name, unicode_name=None,
                 flat_name=None, unicode_flat_name=None,
                 sharp_name=None, unicode_sharp_name=None):

        self._step = step
        self._name = name
        self._unicode_name = unicode_name
        self._flat_name = flat_name
        self._unicode_flat_name = unicode_flat_name
        self._sharp_name = sharp_name
        self._unicode_sharp_name = unicode_sharp_name

    ##############################################

    @property
    def step(self):
        return self._step

    @property
    def name(self):
        return self._name

    @property
    def unicode_name(self):
        if self._unicode_name is None:
            return self._name
        else:
            return self._unicode_name

    @property
    def flat_name(self):
        return self._flat_name

    @property
    def unicode_flat_name(self):
        return self._unicode_flat_name

    @property
    def sharp_name(self):
        return self._sharp_name

    @property
    def unicode_sharp_name(self):
        return self._unicode_sharp_name

####################################################################################################

# Names of notes in various languages and countries for the 12-tone chromatic scale
__et12_note_name_translations__ = {
    'english': (
        dict(name='C', sharp_name='B sharp', unicode_sharp_name='B♯'),
 	dict(name='C sharp', unicode_name='C♯', flat_name='D flat', unicode_flat_name='D♭'),
 	dict(name='D'),
 	dict(name='D sharp', unicode_name='D♯', flat_name='E flat', unicode_flat_name='E♭'),
 	dict(name='E'),
 	dict(name='F'),
 	dict(name='F sharp', unicode_name='F♯', flat_name='G flat', unicode_flat_name='G♭'),
 	dict(name='G'),
 	dict(name='G sharp', unicode_name='G♯', flat_name='A flat', unicode_flat_name='A♭'),
 	dict(name='A'),
 	dict(name='A sharp', unicode_name='A♯', flat_name='B flat', unicode_flat_name='B♭'),
 	dict(name='B'),
    ),
    'deutsch': (
        dict(name='C', sharp_name='His', unicode_sharp_name='H♯'),
 	dict(name='Cis', unicode_name='C♯', flat_name='Des', unicode_flat_name='D♭'),
 	dict(name='D'),
 	dict(name='Dis', unicode_name='D♯', flat_name='Ees', unicode_flat_name='E♭'),
 	dict(name='E'),
 	dict(name='F'),
 	dict(name='Fis', unicode_name='F♯', flat_name='Ges', unicode_flat_name='G♭'),
 	dict(name='G'),
 	dict(name='Gis', unicode_name='G♯', flat_name='Aes', unicode_flat_name='A♭'),
 	dict(name='A'),
 	dict(name='Ais', unicode_name='A♯', flat_name='Bes', unicode_flat_name='B♭'),
 	dict(name='H'),
    ),
    'nederlands': ( # Fixme: Right ???
        dict(name='C', sharp_name='B sharp', unicode_sharp_name='B♯'),
 	dict(name='Cis', unicode_name='C♯', flat_name='Des', unicode_flat_name='D♭'),
 	dict(name='D'),
 	dict(name='Dis', unicode_name='D♯', flat_name='Ees', unicode_flat_name='E♭'),
 	dict(name='E'),
 	dict(name='F'),
 	dict(name='Fis', unicode_name='F♯', flat_name='Ges', unicode_flat_name='G♭'),
 	dict(name='G'),
 	dict(name='Gis', unicode_name='G♯', flat_name='Aes', unicode_flat_name='A♭'),
 	dict(name='A'),
 	dict(name='Ais', unicode_name='A♯', flat_name='Bes', unicode_flat_name='B♭'),
 	dict(name='B'),
    ),
    'français': (
        dict(name='Do', sharp_name='Si dièse', unicode_sharp_name='Si♯'),
 	dict(name='Do dièse', unicode_name='Do♯', flat_name='Ré bémol', unicode_flat_name='Ré♭'),
 	dict(name='Ré'),
 	dict(name='Ré dièse', unicode_name='Ré♯', flat_name='Mi bémol', unicode_flat_name='Mi♭'),
 	dict(name='Mi'),
 	dict(name='Fa'),
 	dict(name='Fa dièse', unicode_name='Fa♯', flat_name='Sol bémol', unicode_flat_name='Sol♭'),
 	dict(name='Sol'),
 	dict(name='Sol dièse', unicode_name='Sol♯', flat_name='La bémol', unicode_flat_name='La♭'),
 	dict(name='La'),
 	dict(name='La dièse', unicode_name='La♯', flat_name='Si bémol', unicode_flat_name='Si♭'),
 	dict(name='Si'),
    ),
    'italiano': (
        dict(name='Do', sharp_name='Si diesis', unicode_sharp_name='Si♯'),
 	dict(name='Do diesis', unicode_name='Do♯', flat_name='Re bemolle', unicode_flat_name='Re♭'),
 	dict(name='Re'),
 	dict(name='Re diesis', unicode_name='Re♯', flat_name='Mi bemolle', unicode_flat_name='Mi♭'),
 	dict(name='Mi'),
 	dict(name='Fa'),
 	dict(name='Fa diesis', unicode_name='Fa♯', flat_name='Sol bemolle', unicode_flat_name='Sol♭'),
 	dict(name='Sol'),
 	dict(name='Sol diesis', unicode_name='Sol♯', flat_name='La bemolle', unicode_flat_name='La♭'),
 	dict(name='La'),
 	dict(name='La diesis', unicode_name='La♯', flat_name='Si bemolle', unicode_flat_name='Si♭'),
 	dict(name='Si'),
    ),
    'español': (
        dict(name='Do', sharp_name='Si sostenido', unicode_sharp_name='Si♯'),
 	dict(name='Do sostenido', unicode_name='Do♯', flat_name='Re bemol', unicode_flat_name='Re♭'),
 	dict(name='Re'),
 	dict(name='Re sostenido', unicode_name='Re♯', flat_name='Mi bemol', unicode_flat_name='Mi♭'),
 	dict(name='Mi'),
 	dict(name='Fa'),
 	dict(name='Fa sostenido', unicode_name='Fa♯', flat_name='Sol bemol', unicode_flat_name='Sol♭'),
 	dict(name='Sol'),
 	dict(name='Sol sostenido', unicode_name='Sol♯', flat_name='La bemol', unicode_flat_name='La♭'),
 	dict(name='La'),
 	dict(name='La sostenido', unicode_name='La♯', flat_name='Si bemol', unicode_flat_name='Si♭'),
 	dict(name='Si'),
    ),
}

####################################################################################################

# Convert dict to NoteNameTranslation
for language, data in __et12_note_name_translations__.items():
    new_data = [NoteNameTranslation(i, **kwargs) for i, kwargs in enumerate(data)]
    __et12_note_name_translations__[language] = tuple(new_data)

####################################################################################################

class NoteName:

    ##############################################

    def __init__(self, step):

        self._step = step
        self._translations = dict()

    ##############################################

    def __repr__(self):

        return 'Note #{0._step}'.format(self)

    ##############################################

    @property
    def step(self):
        return self._step

    ##############################################

    @property
    def languages(self):

        return self._translations.keys()

    ##############################################

    def __getitem__(self, language):

        return self._translations[language]

    ##############################################

    def add_language(self, language, translation):

        self._translations[language] = translation

####################################################################################################

#: List of NoteName for 12-TET
ET12_NOTE_NAMES = [NoteName(step) for step in range(12)]
for language, data in __et12_note_name_translations__.items():
    for note in ET12_NOTE_NAMES:
        note.add_language(language, data[note.step])

_et12_note_names_map = {}
for note in ET12_NOTE_NAMES:
    for language in note.languages:
        note_translation = note[language]
        for attribute in ('name', 'unicode_name',
                          'flat_name', 'unicode_flat_name',
                          'sharp_name', 'unicode_sharp_name'):
            name = getattr(note_translation, attribute)
            if name is not None and name not in _et12_note_names_map:
                _et12_note_names_map[name] = note

def translate_et12_note(name):
    if isinstance(name, int):
        return ET12_NOTE_NAMES[name]
    else:
        return _et12_note_names_map[name]
