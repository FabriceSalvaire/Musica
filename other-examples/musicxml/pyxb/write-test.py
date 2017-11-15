####################################################################################################

import Musica.MusicXML.Pyxb as MusicXML

####################################################################################################

Part = MusicXML.CTD_ANON_
Measure = MusicXML.CTD_ANON_4

####################################################################################################

# <?xml version="1.0" encoding="UTF-8"?>
# <!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">
# <score-partwise>

# The score-partwise element is the root element for a partwise MusicXML score. It includes a
# score-header group followed by a series of parts with measures inside. The document-attributes
# attribute group includes the version attribute.

score_partwise = MusicXML.score_partwise()
# MusicXML.CTD_ANON

#   <work>
#     <work-title>Title</work-title>
#   </work>
work = MusicXML.work(work_title='Title')
score_partwise.work = work
#work.work_title = 'Title'

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

identification = MusicXML.identification()
score_partwise.identification = identification
# identification.creator.append(MusicXML.typed_text('Composer', type='composer'))
identification.creator.extend([
    MusicXML.typed_text('Composer', type='composer'),
    MusicXML.typed_text('Lyricist', type='lyricist'),
])
identification.rights.append('Copyright')
encoding = MusicXML.encoding()
identification.encoding = encoding
encoding.software.append('MuseScore 2.1.0')
encoding.encoding_date.append(MusicXML.yyyy_mm_dd(2017, 10, 14))
encoding.supports.extend([
    MusicXML.supports(element='accidental', type='yes'),
    MusicXML.supports(element='beam', type='yes'),
    MusicXML.supports(element='print', attribute='new-page', type='yes', value_='yes'),
    MusicXML.supports(element='print', attribute='new-system', type='yes', value_='yes'),
    MusicXML.supports(element='stem', type='yes'),
])

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

defaults = MusicXML.defaults()
score_partwise.defaults = defaults
defaults.scaling = MusicXML.scaling(millimeters=7.05556, tenths=40)
page_layout = MusicXML.page_layout(page_height=1683.36, page_width=1190.88)
defaults.page_layout = page_layout
page_layout.page_margins.extend([
    MusicXML.page_margins(type='even',
                          left_margin=56.6929,
                          right_margin=56.6929,
                          top_margin=56.6929,
                          bottom_margin=113.386),
    MusicXML.page_margins(type='odd',
                          left_margin=56.6929,
                          right_margin=56.6929,
                          top_margin=56.6929,
                          bottom_margin=113.386),
    ])
defaults.word_font = MusicXML.empty_font(font_family='FreeSerif', font_size=10)
defaults.lyric_font.append(MusicXML.lyric_font(font_family='FreeSerif', font_size=11))

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

####################################################################################################

# score-partwise must have a part-list

# The part-list identifies the different musical parts in this movement. Each part has an ID that is
# used later within the musical data. Since parts may be encoded separately and combined later,
# identification elements are present at both the score and score-part levels. There must be at
# least one score-part, combined as desired with part-group elements that indicate braces and
# brackets. Parts are ordered from top to bottom in a score based on the order in which they appear
# in the part-list.

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

part_list = MusicXML.part_list()
score_partwise.part_list = part_list

part_group = MusicXML.part_group(type='start', number='1')
part_group.group_symbol = 'none'
part_list.part_group.append(part_group)

score_part = MusicXML.score_part(id='P1')
part_list.score_part.append(score_part)
score_part.part_name = 'Guitar'
score_part.part_abbreviation = 'Guit.'

# Fixme: accolade
part_list.part_group.append(MusicXML.part_group(type='stop', number='1'))

####################################################################################################

# score-partwise must have at least one part

#   <part id="P1">
part = Part(id='P1')
score_partwise.part.append(part)

#     <measure number="1" width="515.32">
measure = Measure(number=1, width='515.32')
part.measure.append(measure)

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
print_ = MusicXML.print_()
# measure.print_.append(print_)
measure.append(print_)
system_layout = MusicXML.system_layout()
print_.system_layout = system_layout
system_layout.system_margins = MusicXML.system_margins(left_margin=0, right_margin=0)
system_layout.top_system_distance = 170
staff_layout = MusicXML.staff_layout(number=2, staff_distance=65)
print_.staff_layout.append(staff_layout)

#       <attributes>
attributes = MusicXML.attributes() # divisions=8
# measure.attributes.append(attributes)
measure.append(attributes)
#         <divisions>8</divisions>
attributes.divisions = 8

#         <key>
#           <fifths>0</fifths>
#         </key>
key = MusicXML.key(fifths=0)
attributes.key.append(key)
# key.fifths = 0

#         <time>
#           <beats>4</beats>
#           <beat-type>4</beat-type>
#         </time>
time = MusicXML.time(beats='4', beat_type='4')
attributes.time.append(time)
# time.beats = '4'
# time.beat_type = '4'

#         <staves>2</staves>
attributes.staves = 2

#         <clef number="1">
#           <sign>G</sign>
#           <line>2</line>
#           <clef-octave-change>-1</clef-octave-change>
#         </clef>
clef = MusicXML.clef(number=1, sign='G', line=2, clef_octave_change=-1)
attributes.clef.append(clef)

#         <clef number="2">
#           <sign>TAB</sign>
#           <line>5</line>
#         </clef>
clef = MusicXML.clef(number=2, sign='TAB', line=5)
attributes.clef.append(clef)

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

staff_details = MusicXML.staff_details(number=2, staff_lines=6)
attributes.staff_details.append(staff_details)
staff_details.staff_tuning.extend([
    MusicXML.staff_tuning(line=1, tuning_step='E', tuning_octave=2),
    MusicXML.staff_tuning(line=2, tuning_step='A', tuning_octave=2),
    MusicXML.staff_tuning(line=3, tuning_step='D', tuning_octave=3),
    MusicXML.staff_tuning(line=4, tuning_step='G', tuning_octave=3),
    MusicXML.staff_tuning(line=5, tuning_step='B', tuning_octave=3),
    MusicXML.staff_tuning(line=6, tuning_step='E', tuning_octave=4),
])

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
direction = MusicXML.direction(placement='above', staff=1)
# measure.direction.append(direction)
measure.append(direction)
direction_type = MusicXML.direction_type()
metronome = MusicXML.metronome(parentheses='no')
metronome.beat_unit.append('quarter')
metronome.per_minute = MusicXML.per_minute(100)
direction_type.metronome = metronome
direction.direction_type.append(direction_type)
direction.sound = MusicXML.sound(tempo=100)

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
# measure.note.append(
measure.append(
    MusicXML.note(
        default_x=76.78,
        default_y=-35.00,
        pitch=MusicXML.pitch(step='F', octave=3),
        duration=8,
        voice='1',
        type='quarter',
        stem='up',
        staff=1,
    )
)

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

# The backup and forward elements are required to coordinate multiple voices in one part, including
# music on multiple staves. The backup type is generally used to move between voices and
# staves. Thus the backup element does not include voice or staff elements. Duration values should
# always be positive, and should not cross measure boundaries or mid-measure changes in the
# divisions value.

#       <backup>
#         <duration>32</duration>
#       </backup>

# measure.backup.append(MusicXML.backup(duration=32))
measure.append(MusicXML.backup(duration=32))

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

#   </part> # id P1

# </score-partwise>

####################################################################################################

xml_source = score_partwise.toxml(encoding='utf-8')
# print(xml_source.decode('utf-8'))
with open('out.xml', 'wb') as fh:
    fh.write(xml_source)
