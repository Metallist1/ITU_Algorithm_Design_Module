#!/bin/sh
for FILE in *.txt
do
    echo $FILE
    base=${FILE%.txt}
    python3 ../red-scare-main.py $FILE -1 True

done