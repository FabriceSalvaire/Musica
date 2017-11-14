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
                 outer_radius=4,
                 language='français'):

        super().__init__()

        self.use_library('shapes.arrows')

        diatonic_steps = list(ET12.iter_on_naturals())
        for step in diatonic_steps:
            step.interval = ET12.fold_step_number(step.next_natural.step_number - step.step_number)

        def step_to_angle(step):
            return int((90 - step.step_number / ET12.number_of_steps * 360) % 360)

        def translate_step(step, language):
            return step.translate(language).unicode_name

        self.set_main_font('Latin Modern Sans') # Roman
        self.font_size(12)

        self.coordinate('O', x=0, y=0)

        self.define('ArrowRadius', inner_radius - .5, 'cm')
        self.define('InnerRadius', inner_radius, 'cm')
        self.define('MiddleRadius', (inner_radius + outer_radius)/2, 'cm')
        self.define('OuterRadius', outer_radius, 'cm')
        self.define('OuterLabelRadius', outer_radius + 1, 'cm')

        # 360 / 6 = 60 for 2 semitone

        for step in diatonic_steps:
            angle = step_to_angle(step)
            self.coordinate('i{}'.format(step.name), r=r'\InnerRadius', a=angle)
            self.coordinate('o{}'.format(step.name), r=r'\OuterRadius', a=angle)
            self.coordinate('l{}'.format(step.name), r=r'\OuterLabelRadius', a=angle)
            # angle = (step_to_angle(step) + step_to_angle(next_step))/2
            angle = step_to_angle(step) - step.interval * 15 # interval / 2 * 30
            if step.interval == 2:
                self.coordinate('l{}b'.format(step.name), r=r'\OuterLabelRadius', a=angle)
            self.coordinate('m{}'.format(step.name), r=r'\MiddleRadius', a=angle)

        # Fixme: move to tikz ???
        self.new_command('Sector', 3,
                           r'\fill[fill=gray!#1] (#2:\InnerRadius) -- (#2:\OuterRadius) arc (#2:#3:\OuterRadius) -- (#3:\InnerRadius) arc (#3:#2:\InnerRadius);')
        for step in diatonic_steps:
            colour = 20 if step.interval == 1 else 40
            next_step = step.next_natural
            _angle1 = step_to_angle(step)
            _angle2 = step_to_angle(next_step)
            if abs(_angle1 - _angle2) > 60:
                angle1 = _angle1
                angle2 = _angle2 - 360
            else:
                angle1 = min(_angle1, _angle2)
                angle2 = max(_angle1, _angle2)
            self.append(self.format(r'\Sector{«0»}{«1»}{«2»};', colour, angle1, angle2))

        for step in diatonic_steps:
            self.line('i{}'.format(step.name), 'o{}'.format(step.name))
        self.draw_circle('O', radius=r'\InnerRadius')
        self.draw_circle('O', radius=r'\OuterRadius')

        for step in diatonic_steps:
            step_text = translate_step(step, language)
            self.text('l{}'.format(step.name), step_text)
            if step.interval == 1:
                interval_text = '1/2'
            else:
                interval_text = '1'
                next_step = step.next_natural
                next_step_text = translate_step(next_step, language)
                text = r'{}$\sharp$/{}$\flat$'.format(step_text, next_step_text)
                self.text('l{}b'.format(step.name), text)
            self.text('m{}'.format(step.name), interval_text)

        self.append_command('draw', r'[->,line width=2pt] (90:\ArrowRadius) arc (90:45:\ArrowRadius)')
