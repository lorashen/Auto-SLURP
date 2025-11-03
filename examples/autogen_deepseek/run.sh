#!/bin/bash
for f in $(seq 0 999);
do
    echo $f
    timeout 240s python3 test.py $f > $f.log
done
