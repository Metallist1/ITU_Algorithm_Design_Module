#!/bin/sh
for FILE in *-in.txt

do
	echo $FILE
	base=${FILE%-in.txt}
    python3 ../solution/stable_matching.py $FILE
    diff $base-test.out.txt $base-out.txt
done
