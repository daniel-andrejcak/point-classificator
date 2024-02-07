#! /bin/bash

echo "Success rates" > testing_output.txt

for seed in 12345 54321 98765; do
    if [ "$1" == "-nn" ]; then
        python nn.py  -s $seed -f --save

    else
        for k in 1 3 7 15; do
            python main.py -k $k -s $seed -f --save >> testing_output.txt
        done
    fi

done
