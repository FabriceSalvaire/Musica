python objectifier-test.py
python musicxml-example.py

option='--schema musicxml.xsd'
for i in out.xml out2.xml; do
  xmllint ${option} --format $i -o $i
done

diff -Naur musicxml-samples/example1.xml out.xml | less
diff -Naur out.xml out2.xml | less
