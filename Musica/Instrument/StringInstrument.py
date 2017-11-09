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

import os

# from ..Theory.Temperament import ET12
from ..Theory.Pitch import Pitch
from .Instrument import Instrument

####################################################################################################

class String:

    ##############################################

    def __init__(self, pitch, length):

        self._pitch = pitch
        self._length = length

    ##############################################

    @property
    def pitch(self):
        return self._pitch

    @property
    def length(self):
        return self._length

    ##############################################

    def __eq__(self, other):
        return self._pitch == other.pitch and self._length == other.length

    ##############################################

    def fret_position(self, i, from_nut=True):

        # From nut / sillet

        position = self._length * 2**(-i/self._pitch.temperament.number_of_steps)
        if from_nut:
            position = self._length - position

        return position

####################################################################################################

class StringTuning:

    ##############################################

    def __init__(self, instrument, name, pitches):

        self._instrument = instrument
        self._name = name
        self._pitches = pitches

    ##############################################

    @property
    def instrument(self):
        return self._instrument

    @property
    def name(self):
        return self._name

    @property
    def number_of_strings(self):
        return len(self._pitches)

    @property
    def pitches(self):
        return self._pitches

    @property
    def lowest_pitche(self):
        return self._pitches[0]

    @property
    def highest_pitche(self):
        return self._pitches[-1]

    ##############################################

    def __repr__(self):

        return '{} {} [{}]'.format(
            self._instrument.name,
            self._name,
            ', '.join([pitch.full_name for pitch in self._pitches])
        )

    ##############################################

    def __eq__(self, other):
        return self._pitches == other.pitches

    ##############################################

    def __len__(self):
        return len(self._pitches)

    ##############################################

    def __iter__(self):
        return iter(self._pitches)

    ##############################################

    def __getitem__(self, index):

        if isinstance(index, Pitch):
            string = self._pitches.find(index)
            if string == -1:
                raise IndexError()
            else:
                return string
        else:
            return self._pitches[index]

####################################################################################################

class InstrumentTunings:

    ##############################################

    def __init__(self, name, **tunings):

        self._name = name
        self._tunings = {}

        for tuning_name, pitches in tunings.items():
            self.add(tuning_name, pitches)

    ##############################################

    @property
    def name(self):
        return self._name

    @property
    def tunings(self):
        return self._tunings.keys()

    ##############################################

    def __iter__(self):
        return iter(self._tunings.values())

    ##############################################

    def __getitem__(self, tuning_name):
        return self._tunings[tuning_name]

    ##############################################

    def add(self, name, pitches):

        if name not in self._tunings:
            if isinstance(pitches, str):
                if '...' in pitches:
                    start_pitch, last_pitch = [Pitch(pitch.strip()) for pitch in pitches.split('...')]
                    pitches = [pitch for pitch in start_pitch.pitch_iterator(last_pitch)]
                else:
                    pitches = [Pitch(pitch) for pitch in pitches.split()]
            self._tunings[name] = StringTuning(self, name, pitches)
        else:
            raise NameError("Tuning {} already exists".format(name))

####################################################################################################

class StringInstrumentTuningDatabase:

    ___instance__ = None

    ##############################################

    @classmethod
    def instance(cls):

        if cls.___instance__ is None:
            yaml_path = os.path.join(os.path.dirname(__file__), 'stringed-instrument-tunings.yml')
            cls.___instance__ = cls(yaml_path)

        return cls.___instance__

    ##############################################

    def __init__(self, yaml_path):

        self._yaml_path = yaml_path
        self._instruments = {}

        self._load()

    ##############################################

    def _load(self):

        import yaml
        with open(self._yaml_path, 'r') as fh:
            instruments = yaml.load(fh)

        self._instruments = {instrument:InstrumentTunings(instrument, **tunings)
                             for instrument, tunings in instruments.items()}

    ##############################################

    @property
    def instruments(self):
        return self._instruments.keys()

    ##############################################

    def __getitem__(self, instrument):
        return self._instruments[instrument]

####################################################################################################

class StringInstrument(Instrument):

    ##############################################

    def __init__(self,
                 name,
                 category,
                 standard_tuning):

        super().__init__(name, category)

        self._standard_tuning = standard_tuning
        self._tuning = standard_tuning

    ##############################################

    @property
    def standard_tuning(self):
        return self._standard_tuning

    @property
    def number_of_strings(self):
        return len(self._standard_tuning)

    @property
    def tuning(self):
        return self._tuning

    @tuning.setter
    def tuning(self, value):
        self._tuning = value

    @property
    def lowest_pitche(self):
        return self._tuning.lowest_pitche

    @property
    def highest_pitche(self):
        raise NotImplementedError
        # return self._tuning.highest_pitche

####################################################################################################

# class Guitare(StringInstrument):

#     ##############################################

#     def __init__():

#         super().__init__(
#             name='guitare',
#             category='fretted string/guitare',
#             standard_tuning=GuitareTuning.standard,
#         )
