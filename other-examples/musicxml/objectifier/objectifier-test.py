####################################################################################################

from Musica.Xml.Objectifier import XmlObjectifierFactory

####################################################################################################

doctype = '<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.0 Partwise//EN" "http://www.musicxml.org/dtds/partwise.dtd">'
factory = XmlObjectifierFactory(doctype=doctype)

####################################################################################################

# .mxl is a zip azchive

file_path = 'musicxml-samples/example1.xml'
root = factory.parse(file_path)

####################################################################################################

root.write_xml('out.xml', doctype=doctype)

####################################################################################################

with open('MusicXML.py', 'w') as output:
    output.write('from Musica.Xml.Objectifier import XmlObjectifierNode, XmlObjectifierLeaf\n')
    for cls in sorted(factory, key=lambda cls: cls.__name__):
        output.write(cls.class_to_python() + '\n')

with open('musicxml-example.py', 'w') as output:
    output.write('from MusicXML import *\n\n')
    output.write(root.to_python() + '\n')
    output.write('\n')
    output.write("score_partwise_0.write_xml('out2.xml', doctype='{}')\n".format(doctype))

####################################################################################################

# for cls in factory:
#     print(cls.__name__, cls.__attribute_names__, cls.__child_names__)

# for item in root:
#     print(item)

# for credit in root.credit:
#     print(credit.to_xml())

# for part in root.Part:
#     for measure in part.Measure:
#         for note in measure.Note:
#             print(note.Pitch[0].Step[0].text)
