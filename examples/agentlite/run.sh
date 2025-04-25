#!/bin/bash
for f in $(seq 96 96);
do
    echo $f
    timeout 240s python3 example/iot_manager.py $f > $f.log
done
