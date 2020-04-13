#!/bin/bash

for f in *.py
do
  if [ "$f" != "generate_images.py" ]
  then
    python "$f" &
  fi
done

wait

python generate_images.py