#!/bin/bash
for x in `find ./data/csv -name *201*.csv`;
do
   python postgres_populate.py $x
done
