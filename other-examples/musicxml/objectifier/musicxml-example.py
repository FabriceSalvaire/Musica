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

from MusicXML import *

####################################################################################################

score_partwise_0 = ScorePartwise()

score_partwise_0.append(

    Work(
        WorkTitle('Title'),
    ),

    Identification(
        Creator('Composer', type='composer'),
        Creator('Lyricist', type='lyricist'),
        Rights('Copyright'),
        Encoding(
            Software('MuseScore 2.1.0'),
            EncodingDate('2017-10-14'),
            Supports(element='accidental', type='yes'),
            Supports(element='beam', type='yes'),
            Supports(attribute='new-page', element='print', type='yes', value='yes'),
            Supports(attribute='new-system', element='print', type='yes', value='yes'),
            Supports(element='stem', type='yes'),
        ),
    ),

    Defaults(
        Scaling(
            Millimeters(7.05556),
            Tenths(40),
        ),
        PageLayout(
            PageHeight(1683.36),
            PageWidth(1190.88),
            PageMargins(
                type='even',
                childs=(
                    LeftMargin(56.6929),
                    RightMargin(56.6929),
                    TopMargin(56.6929),
                    BottomMargin(113.386),
                )
            ),
            PageMargins(
                type='odd',
                childs=(
                    LeftMargin(56.6929),
                    RightMargin(56.6929),
                    TopMargin(56.6929),
                    BottomMargin(113.386),
                )
            ),
        ),
        WordFont(font_family='FreeSerif', font_size=10),
        LyricFont(font_family='FreeSerif', font_size=11),
    ),

    Credit(
        page=1,
        childs=(
            CreditWords('Title', default_x=595.44, default_y=1626.67, font_size=24, justify='center', valign='top'),
        )
    ),
    Credit(
        page=1,
        childs=(
            CreditWords('Subtitle', default_x=595.44, default_y=1569.97, font_size=14, justify='center', valign='top'),
        )
    ),
    Credit(
        page=1,
        childs=(
            CreditWords('Composer', default_x=1134.19, default_y=1526.67, font_size=12, justify='right', valign='bottom'),
        )
    ),
    Credit(
        page=1,
        childs=(
            CreditWords('Lyricist', default_x=56.6929, default_y=1526.67, font_size=12, justify='left', valign='bottom'),
        )
    ),
    Credit(
        page=1,
        childs=(
            CreditWords('Copyright', default_x=595.44, default_y=113.386, font_size=8, justify='center', valign='bottom'),
        )
    ),

    PartList(
        PartGroup(
            number=1, type='start',
            childs=(
                GroupSymbol('none'),
            )
        ),
        ScorePart(
            id='P1',
            childs=(
                PartName('Guitar'),
                PartAbbreviation('Guit.'),
                ScoreInstrument(
                    id='P1-I1',
                    childs=(
                        InstrumentName('Classical Guitar'),
                    )
                ),
                MidiDevice(id='P1-I1', port=1),
                MidiInstrument(
                    id='P1-I1',
                    childs=(
                        MidiChannel(1),
                        MidiProgram(25),
                        Volume(78.7402),
                        Pan(0),
                    )
                ),
            )
        ),
        PartGroup(number=1, type='stop'),
    ),
)

####################################################################################################

part_0 = Part(id='P1')

####################################################################################################

measure_0 = Measure(
    number=1,
    childs=(
        Print(
            SystemLayout(
                SystemMargins(
                    LeftMargin(0.0),
                    RightMargin(-0.0),
                ),
                TopSystemDistance(170.0),
            ),
            StaffLayout(
                number=2,
                childs=(
                    StaffDistance(65.0),
                )
            ),
        ),

        Attributes(
            Divisions(8),
            Key(
                Fifths(0),
            ),
            Time(
                Beats(4),
                BeatType(4),
            ),
            Staves(2),
            Clef(
                number=1,
                childs=(
                    Sign('G'),
                    Line(2),
                    ClefOctaveChange(-1),
                )
            ),
            Clef(
                number=2,
                childs=(
                    Sign('TAB'),
                    Line(5),
                )
            ),
            StaffDetails(
                number=2,
                childs=(
                    StaffLines(6),
                    StaffTuning(
                        line=1,
                        childs=(
                            TuningStep('E'),
                            TuningOctave(2),
                        )
                    ),
                    StaffTuning(
                        line=2,
                        childs=(
                            TuningStep('A'),
                            TuningOctave(2),
                        )
                    ),
                    StaffTuning(
                        line=3,
                        childs=(
                            TuningStep('D'),
                            TuningOctave(3),
                        )
                    ),
                    StaffTuning(
                        line=4,
                        childs=(
                            TuningStep('G'),
                            TuningOctave(3),
                        )
                    ),
                    StaffTuning(
                        line=5,
                        childs=(
                            TuningStep('B'),
                            TuningOctave(3),
                        )
                    ),
                    StaffTuning(
                        line=6,
                        childs=(
                            TuningStep('E'),
                            TuningOctave(4),
                        )
                    ),
                )
            ),
        ),
        Direction(
            placement='above',
            childs=(
                DirectionType(
                    Metronome(
                        parentheses='no',
                        childs=(
                            BeatUnit('quarter'),
                            PerMinute(100),
                        )
                    ),
                ),
                Staff(1),
                Sound(tempo=100),
            )
        ),

    ##############################################

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('up'),
            Staff(1),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('up'),
            Staff(1),
        ),

        Note(
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('down'),
            Staff(1),
        ),
        Note(
            Chord(),
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('down'),
            Staff(1),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('down'),
            Staff(1),
        ),
        Note(
            Chord(),
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('down'),
            Staff(1),
        ),
        Note(
            Chord(),
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('down'),
            Staff(1),
        ),

    ##############################################

        Backup(
            Duration(32),
        ),

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(4),
                    Fret(3),
                ),
            ),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(3),
                    Fret(2),
                ),
            ),
        ),

        Note(
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(2),
                    Fret(1),
                ),
            ),
        ),
        Note(
            Chord(),
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(1),
                    Fret(0),
                ),
            ),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(3),
                    Fret(2),
                ),
            ),
        ),
        Note(
            Chord(),
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(2),
                    Fret(1),
                ),
            ),
        ),
        Note(
            Chord(),
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(1),
                    Fret(0),
                ),
            ),
        ),
    )
)

part_0.append(measure_0)

####################################################################################################

measure_1 = Measure(
    number=2,
    # width=562.18
    childs=(

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(2),
            Voice(1),
            Type('16th'),
            Stem('up'),
            Staff(1),
            Beam('begin', number=1),
            Beam('begin', number=2),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(2),
            Voice(1),
            Type('16th'),
            Stem('up'),
            Staff(1),
            Beam('continue', number=1),
            Beam('end', number=2),
        ),

        Note(
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(4),
            Voice(1),
            Type('eighth'),
            Stem('up'),
            Staff(1),
            Beam('end', number=1),
        ),

        Note(
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(4),
            Voice(1),
            Type('eighth'),
            Stem('down'),
            Staff(1),
            Beam('begin', number=1),
        ),

        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(1),
            Voice(1),
            Type('32nd'),
            Stem('down'),
            Staff(1),
            Beam('end', number=1),
            Beam('backward hook', number=2),
            Beam('backward hook', number=3),
        ),

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Tie(type='start'),
            Voice(1),
            Type('quarter'),
            Stem('up'),
            Staff(1),
            Notations(
                Tied(type='start'),
            ),
        ),
        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Tie(type='stop'),
            Voice(1),
            Type('quarter'),
            Stem('up'),
            Staff(1),
            Notations(
                Tied(type='stop'),
            ),
        ),
        Note(
            Chord(),
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(1),
            Type('quarter'),
            Stem('up'),
            Staff(1),
        ),
        Note(
            Pitch(
                Step('B'),
                Octave(3),
            ),
            Duration(2),
            Voice(1),
            Type('16th'),
            Stem('up'),
            Staff(1),
            Beam('begin', number=1),
            Beam('begin', number=2),
        ),

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(1),
            Voice(1),
            Type('32nd'),
            Stem('up'),
            Staff(1),
            Beam('end', number=1),
            Beam('end', number=2),
            Beam('backward hook', number=3),
        ),

    ##############################################

        Backup(
            Duration(32),
        ),

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(2),
            Voice(5),
            Type('16th'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(4),
                    Fret(3),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(2),
            Voice(5),
            Type('16th'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(3),
                    Fret(2),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('C'),
                Octave(4),
            ),
            Duration(4),
            Voice(5),
            Type('eighth'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(2),
                    Fret(1),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('E'),
                Octave(4),
            ),
            Duration(4),
            Voice(5),
            Type('eighth'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(1),
                    Fret(0),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(1),
            Voice(5),
            Type('32nd'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(3),
                    Fret(2),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Tie(type='start'),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Tied(type='start'),
                Technical(
                    String(4),
                    Fret(3),
                ),
            ),
        ),
        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(8),
            Tie(type='stop'),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Tied(type='stop'),
                Technical(
                    String(4),
                    Fret(3),
                ),
            ),
        ),
        Note(
            Chord(),
            Pitch(
                Step('A'),
                Octave(3),
            ),
            Duration(8),
            Voice(5),
            Type('quarter'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(3),
                    Fret(2),
                ),
            ),
        ),

        Note(
            Pitch(
                Step('B'),
                Octave(3),
            ),
            Duration(2),
            Voice(5),
            Type('16th'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(2),
                    Fret(0),
                ),
            ),
        ),

        Note(
            Pitch(
                Step('F'),
                Octave(3),
            ),
            Duration(1),
            Voice(5),
            Type('32nd'),
            Stem('none'),
            Staff(2),
            Notations(
                Technical(
                    String(4),
                    Fret(3),
                ),
            ),
        ),

    ##############################################

        Barline(
            location='right',
            childs=(
                BarStyle('light-heavy'),
            )
        ),
    )
)

part_0.append(measure_1)

####################################################################################################

score_partwise_0.append(part_0)

####################################################################################################

doctype='<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'
score_partwise_0.write_xml('out.xml', doctype=doctype)
