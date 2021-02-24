#!/bin/bash

for f in *.py
do
  if [ "$f" != "generate_images.py" ]
  then
    echo $f
    python "$f" & 
  fi
done

wait



#!/bin/bash

for f in *.py
  do
     PYTHONPATH=../ python $f &
  done
[user]
        name = Pierre Schaus
        email = pschaus@gmail.com
#python generate_images.py
