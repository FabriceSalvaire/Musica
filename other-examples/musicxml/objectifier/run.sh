input=musicxml-samples/samples/example1.xml
musicxml-to-python ${input} out-ref.xml
musicxml-to-python --add-write-xml ${input} out.py
python out.py

option='--schema musicxml.xsd'
for i in out-ref.xml out.xml; do
  xmllint ${option} --format $i -o $i
done

diff -Naur ${input} out-ref.xml | less
diff -Naur out-ref.xml out.xml | less
