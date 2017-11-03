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
    'DiatonicScale',
    ]

####################################################################################################

from ..Theory.Pitch import ET12, Pitch
from ..Tex.Tikz import TikzFigure

####################################################################################################

class DiatonicScale(TikzFigure):

    ##############################################

    def __init__(self,
                 inner_radius=3,
                 outer_radius=4):

        super().__init__()

        self.use_library('shapes.arrows')

        diatonic_pitches = [Pitch(step) for step in ET12.step_names]
        for i, pitch in enumerate(diatonic_pitches):
            setattr(pitch, 'rank', i)

        def pitch_to_angle(pitch):
            return int((90 - pitch.pitch_class / 12 * 360) % 360)

        def next_pitch_of(pitch):
            return diatonic_pitches[(pitch.rank+1) % len(diatonic_pitches)]

        intervales = [(next_pitch_of(pitch).pitch_class - pitch.pitch_class) % 12
                      for pitch in diatonic_pitches]

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(12)

        self.coordinate('O', x=0, y=0)

        self.define('ArrowRadius', inner_radius - .5, 'cm')
        self.define('InnerRadius', inner_radius, 'cm')
        self.define('MiddleRadius', (inner_radius + outer_radius)/2, 'cm')
        self.define('OuterRadius', outer_radius, 'cm')
        self.define('OuterLabelRadius', outer_radius + 1, 'cm')

        # 360 / 6 = 60 for 2 semitone

        for pitch, interval in zip(diatonic_pitches, intervales):
            angle = pitch_to_angle(pitch)
            self.coordinate('i{}'.format(pitch), r='\InnerRadius', a=angle)
            self.coordinate('o{}'.format(pitch), r='\OuterRadius', a=angle)
            self.coordinate('l{}'.format(pitch), r='\OuterLabelRadius', a=angle)
            # next_pitch = next_pitch_of(pitch)
            # angle = (pitch_to_angle(pitch) + pitch_to_angle(next_pitch))/2
            angle = pitch_to_angle(pitch) - interval * 15 # interval / 2 * 30
            if interval == 2:
                self.coordinate('l{}b'.format(pitch), r='\OuterLabelRadius', a=angle)
            self.coordinate('m{}'.format(pitch.step), r='\MiddleRadius', a=angle)

        self.new_command('Sector', 3,
                           r'\fill[fill=gray!#1] (#2:\InnerRadius) -- (#2:\OuterRadius) arc (#2:#3:\OuterRadius) -- (#3:\InnerRadius) arc (#3:#2:\InnerRadius);')
        for pitch, interval in zip(diatonic_pitches, intervales):
            colour = 20 if interval == 1 else 40
            next_pitch = next_pitch_of(pitch)
            _angle1 = pitch_to_angle(pitch)
            _angle2 = pitch_to_angle(next_pitch)
            if abs(_angle1 - _angle2) > 60:
                angle1 = _angle1
                angle2 = _angle2 - 360
            else:
                angle1 = min(_angle1, _angle2)
                angle2 = max(_angle1, _angle2)
            self.append(self.format(r'\Sector{«0»}{«1»}{«2»};', colour, angle1, angle2))

        for pitch in diatonic_pitches:
            self.line('i{}'.format(pitch), 'o{}'.format(pitch))
        self.append_command(r'\draw (O) circle (\InnerRadius)')
        self.append_command(r'\draw (O) circle (\OuterRadius)')

        for pitch, interval in zip(diatonic_pitches, intervales):
            pitch_text = pitch.french_locale.name
            self.node('l{}'.format(pitch), pitch_text)
            if interval == 1:
                interval_text = '1/2'
            else:
                interval_text = '1'
                next_pitch = next_pitch_of(pitch)
                next_pitch_text = next_pitch.french_locale.name
                text = r'{}$\sharp$/{}$\flat$'.format(pitch_text, next_pitch_text)
                self.node('l{}b'.format(pitch), text)
            self.node('m{}'.format(pitch), interval_text)

        self.append_command(r'\draw[->,line width=2pt] (90:\ArrowRadius) arc (90:45:\ArrowRadius)')
