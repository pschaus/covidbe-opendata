#!/bin/bash

for f in *.py
do
  echo $f
  python "$f" &
done
