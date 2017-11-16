python write-test.py
xmllint ${option} --format out2.xml -o out2.xml
diff -Naur out.xml out2.xml | less
musescore out2.xml
