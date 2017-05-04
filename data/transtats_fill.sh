#!/bin/bash
for x in `find ./data/csv -name *2016*.csv`;
do
   python postgres_populate.py $x
done
