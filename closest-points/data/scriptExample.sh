#!/bin/sh
for FILE in *-tsp.txt

do
    echo $FILE
    base=${FILE%-tsp.txt}
    python3 ../closest-pair.py $FILE

done