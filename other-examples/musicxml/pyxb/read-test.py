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

import Musica.MusicXML.Pyxb as MusicXML

####################################################################################################

file_path = 'musicxml-samples/example1.xml'

with open(file_path) as fh:
    musicxml_doc = MusicXML.CreateFromDocument(fh.read())

with open('bootstrap.xml', 'w') as fh:
    fh.write(musicxml_doc.toxml())

####################################################################################################

# <?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
# <score-partwise>

score_partwise = MusicXML.score_partwise()
# MusicXML.CTD_ANON

#   <work>
#     <work-title>Title</work-title>
#   </work>

print('work-tile', musicxml_doc.work.work_title)

#   <identification>
#     <creator type="composer">Composer</creator>
#     <creator type="lyricist">Lyricist</creator>
#     <rights>Copyright</rights>
#     <encoding>
#       <software>MuseScore 2.1.0</software>
#       <encoding-date>2017-10-14</encoding-date>
#       <supports element="accidental" type="yes"/>
#       <supports element="beam" type="yes"/>
#       <supports element="print" attribute="new-page" type="yes" value="yes"/>
#       <supports element="print" attribute="new-system" type="yes" value="yes"/>
#       <supports element="stem" type="yes"/>
#     </encoding>
#   </identification>

identification = musicxml_doc.identification
for creator in identification.creator:
    print('creator', creator.type, creator.value())

encoding = identification.encoding
print('software', encoding.software[0])
print('encoding-date', encoding.encoding_date[0])
for supports in encoding.supports:
    print('supports', supports.element, supports.type)

#   <defaults>
#     <scaling>
#       <millimeters>7.05556</millimeters>
#       <tenths>40</tenths>
#     </scaling>
#     <page-layout>
#       <page-height>1683.36</page-height>
#       <page-width>1190.88</page-width>
#       <page-margins type="even">
#         <left-margin>56.6929</left-margin>
#         <right-margin>56.6929</right-margin>
#         <top-margin>56.6929</top-margin>
#         <bottom-margin>113.386</bottom-margin>
#       </page-margins>
#       <page-margins type="odd">
#         <left-margin>56.6929</left-margin>
#         <right-margin>56.6929</right-margin>
#         <top-margin>56.6929</top-margin>
#         <bottom-margin>113.386</bottom-margin>
#       </page-margins>
#     </page-layout>
#     <word-font font-family="FreeSerif" font-size="10"/>
#     <lyric-font font-family="FreeSerif" font-size="11"/>
#   </defaults>

#   <credit page="1">
#     <credit-words default-x="595.44" default-y="1626.67" justify="center" valign="top" font-size="24">Title</credit-words>
#   </credit>
#   <credit page="1">
#     <credit-words default-x="595.44" default-y="1569.97" justify="center" valign="top" font-size="14">Subtitle</credit-words>
#   </credit>
#   <credit page="1">
#     <credit-words default-x="1134.19" default-y="1526.67" justify="right" valign="bottom" font-size="12">Composer</credit-words>
#   </credit>
#   <credit page="1">
#     <credit-words default-x="56.6929" default-y="1526.67" justify="left" valign="bottom" font-size="12">Lyricist</credit-words>
#   </credit>
#   <credit page="1">
#     <credit-words default-x="595.44" default-y="113.386" justify="center" valign="bottom" font-size="8">Copyright</credit-words>
#   </credit>

for credit in musicxml_doc.credit:
    print(credit.page)
    for credit_words in credit.credit_words:
        print(credit_words.value())

#   <part-list>
#     <part-group type="start" number="1">
#       <group-symbol>none</group-symbol>
#     </part-group>
#     <score-part id="P1">
#       <part-name>Guitar</part-name>
#       <part-abbreviation>Guit.</part-abbreviation>
#       <score-instrument id="P1-I1">
#         <instrument-name>Classical Guitar</instrument-name>
#       </score-instrument>
#       <midi-device id="P1-I1" port="1"></midi-device>
#       <midi-instrument id="P1-I1">
#         <midi-channel>1</midi-channel>
#         <midi-program>25</midi-program>
#         <volume>78.7402</volume>
#         <pan>0</pan>
#       </midi-instrument>
#     </score-part>
#     <part-group type="stop" number="1"/>
#   </part-list>

part_list = musicxml_doc.part_list
for part_group in part_list.part_group:
    print('part-group', part_group.type, part_group.number)
    if part_group.group_symbol:
        print(part_group.group_symbol.value())
for score_part in part_list.score_part:
    print(score_part.part_name.value())
    print(score_part.part_abbreviation.value())

#   <part id="P1">
#     <measure number="1" width="515.32">
#       <print>
#         <system-layout>
#           <system-margins>
#             <left-margin>0.00</left-margin>
#             <right-margin>-0.00</right-margin>
#           </system-margins>
#           <top-system-distance>170.00</top-system-distance>
#         </system-layout>
#         <staff-layout number="2">
#           <staff-distance>65.00</staff-distance>
#         </staff-layout>
#       </print>
#       <attributes>
#         <divisions>8</divisions>
#         <key>
#           <fifths>0</fifths>
#         </key>
#         <time>
#           <beats>4</beats>
#           <beat-type>4</beat-type>
#         </time>
#         <staves>2</staves>
#         <clef number="1">
#           <sign>G</sign>
#           <line>2</line>
#           <clef-octave-change>-1</clef-octave-change>
#         </clef>
#         <clef number="2">
#           <sign>TAB</sign>
#           <line>5</line>
#         </clef>
#         <staff-details number="2">
#           <staff-lines>6</staff-lines>
#           <staff-tuning line="1">
#             <tuning-step>E</tuning-step>
#             <tuning-octave>2</tuning-octave>
#           </staff-tuning>
#           <staff-tuning line="2">
#             <tuning-step>A</tuning-step>
#             <tuning-octave>2</tuning-octave>
#           </staff-tuning>
#           <staff-tuning line="3">
#             <tuning-step>D</tuning-step>
#             <tuning-octave>3</tuning-octave>
#           </staff-tuning>
#           <staff-tuning line="4">
#             <tuning-step>G</tuning-step>
#             <tuning-octave>3</tuning-octave>
#           </staff-tuning>
#           <staff-tuning line="5">
#             <tuning-step>B</tuning-step>
#             <tuning-octave>3</tuning-octave>
#           </staff-tuning>
#           <staff-tuning line="6">
#             <tuning-step>E</tuning-step>
#             <tuning-octave>4</tuning-octave>
#           </staff-tuning>
#         </staff-details>
#       </attributes>
#       <direction placement="above">
#         <direction-type>
#           <metronome parentheses="no">
#             <beat-unit>quarter</beat-unit>
#             <per-minute>100</per-minute>
#           </metronome>
#         </direction-type>
#         <staff>1</staff>
#         <sound tempo="100"/>
#       </direction>
#       <note default-x="76.78" default-y="-35.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>up</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="186.01" default-y="-25.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>up</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="295.25" default-y="-15.00">
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>down</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="295.25" default-y="-5.00">
#         <chord/>
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>down</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="404.48" default-y="-25.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>down</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="404.48" default-y="-15.00">
#         <chord/>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>down</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="404.48" default-y="-5.00">
#         <chord/>
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>down</stem>
#         <staff>1</staff>
#       </note>
#       <backup>
#         <duration>32</duration>
#       </backup>
#       <note default-x="79.28" default-y="-150.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>4</string>
#             <fret>3</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="188.51" default-y="-135.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>3</string>
#             <fret>2</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="297.75" default-y="-120.00">
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>2</string>
#             <fret>1</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="297.75" default-y="-105.00">
#         <chord/>
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>1</string>
#             <fret>0</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="406.98" default-y="-135.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>3</string>
#             <fret>2</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="406.98" default-y="-120.00">
#         <chord/>
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>2</string>
#             <fret>1</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="406.98" default-y="-105.00">
#         <chord/>
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>1</string>
#             <fret>0</fret>
#           </technical>
#         </notations>
#       </note>
#     </measure>
#     <measure number="2" width="562.18">
#       <note default-x="12.92" default-y="-35.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>1</voice>
#         <type>16th</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <beam number="1">begin</beam>
#         <beam number="2">begin</beam>
#       </note>
#       <note default-x="64.22" default-y="-25.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>1</voice>
#         <type>16th</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <beam number="1">continue</beam>
#         <beam number="2">end</beam>
#       </note>
#       <note default-x="115.52" default-y="-15.00">
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>4</duration>
#         <voice>1</voice>
#         <type>eighth</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <beam number="1">end</beam>
#       </note>
#       <note default-x="186.06" default-y="-5.00">
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>4</duration>
#         <voice>1</voice>
#         <type>eighth</type>
#         <stem>down</stem>
#         <staff>1</staff>
#         <beam number="1">begin</beam>
#       </note>
#       <note default-x="256.60" default-y="-25.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>1</duration>
#         <voice>1</voice>
#         <type>32nd</type>
#         <stem>down</stem>
#         <staff>1</staff>
#         <beam number="1">end</beam>
#         <beam number="2">backward hook</beam>
#         <beam number="3">backward hook</beam>
#       </note>
#       <note default-x="288.66" default-y="-35.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <tie type="start"/>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <notations>
#           <tied type="start"/>
#         </notations>
#       </note>
#       <note default-x="378.44" default-y="-35.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <tie type="stop"/>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <notations>
#           <tied type="stop"/>
#         </notations>
#       </note>
#       <note default-x="378.44" default-y="-25.00">
#         <chord/>
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>1</voice>
#         <type>quarter</type>
#         <stem>up</stem>
#         <staff>1</staff>
#       </note>
#       <note default-x="468.21" default-y="-20.00">
#         <pitch>
#           <step>B</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>1</voice>
#         <type>16th</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <beam number="1">begin</beam>
#         <beam number="2">begin</beam>
#       </note>
#       <note default-x="519.51" default-y="-35.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>1</duration>
#         <voice>1</voice>
#         <type>32nd</type>
#         <stem>up</stem>
#         <staff>1</staff>
#         <beam number="1">end</beam>
#         <beam number="2">end</beam>
#         <beam number="3">backward hook</beam>
#       </note>
#       <backup>
#         <duration>32</duration>
#       </backup>
#       <note default-x="15.42" default-y="-150.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>5</voice>
#         <type>16th</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>4</string>
#             <fret>3</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="66.72" default-y="-135.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>5</voice>
#         <type>16th</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>3</string>
#             <fret>2</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="118.02" default-y="-120.00">
#         <pitch>
#           <step>C</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>4</duration>
#         <voice>5</voice>
#         <type>eighth</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>2</string>
#             <fret>1</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="188.56" default-y="-105.00">
#         <pitch>
#           <step>E</step>
#           <octave>4</octave>
#         </pitch>
#         <duration>4</duration>
#         <voice>5</voice>
#         <type>eighth</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>1</string>
#             <fret>0</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="259.10" default-y="-135.00">
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>1</duration>
#         <voice>5</voice>
#         <type>32nd</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>3</string>
#             <fret>2</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="291.16" default-y="-150.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <tie type="start"/>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <tied type="start"/>
#           <technical>
#             <string>4</string>
#             <fret>3</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="380.94" default-y="-150.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <tie type="stop"/>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <tied type="stop"/>
#           <technical>
#             <string>4</string>
#             <fret>3</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="380.94" default-y="-135.00">
#         <chord/>
#         <pitch>
#           <step>A</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>8</duration>
#         <voice>5</voice>
#         <type>quarter</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>3</string>
#             <fret>2</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="470.71" default-y="-120.00">
#         <pitch>
#           <step>B</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>2</duration>
#         <voice>5</voice>
#         <type>16th</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>2</string>
#             <fret>0</fret>
#           </technical>
#         </notations>
#       </note>
#       <note default-x="522.01" default-y="-150.00">
#         <pitch>
#           <step>F</step>
#           <octave>3</octave>
#         </pitch>
#         <duration>1</duration>
#         <voice>5</voice>
#         <type>32nd</type>
#         <stem>none</stem>
#         <staff>2</staff>
#         <notations>
#           <technical>
#             <string>4</string>
#             <fret>3</fret>
#           </technical>
#         </notations>
#       </note>
#       <barline location="right">
#         <bar-style>light-heavy</bar-style>
#       </barline>
#     </measure>
#   </part>

# </score-partwise>

for part in musicxml_doc.part:
    # part is CTD_ANON_
    print("part {0.id}".format(part))
    for measure in part.measure:
        # measure is CTD_ANON_4
        print("measure {0.number}".format(measure))
        for note in measure.note:
            if note.pitch:
                print("note {1.step}{1.octave} {0.duration} {2}".format(
                    note,
                    note.pitch,
                    'chord' if note.chord is not None else ''))
            for notation in note.notations:
                for technical in notation.technical:
                    if technical.string is not None:
                        print("  {}/{}".format(technical.string[0].value(), technical.fret[0].value()))
