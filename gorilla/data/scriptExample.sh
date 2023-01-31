#!/bin/sh
for FILE in *-in.txt
do
    echo $FILE
    base=${FILE%-in.txt}
    python3 ../gorilla.py $FILE BLOSUM62.txt

done