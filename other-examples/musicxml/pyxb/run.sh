python read-test.py
xmllint -format bootstrap.xml -o bootstrap.xml

python write-test.py
xmllint -format out.xml -o out.xml

# diff example0.xml testf.xml | less
# diff example1.xml testf.xml | less
