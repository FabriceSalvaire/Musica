python musicxml-example.py
xmllint ${option} --format out.xml -o out.xml
diff -Naur out-ref.xml out.xml | less
musescore out.xml
