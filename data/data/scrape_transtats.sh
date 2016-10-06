#!/bin/sh
years=(2016 2015)
months=(1 2 3 4 5 6 7 8 9 10 11 12)

for x in ${years[*]}
do
   for y in ${months[*]}
   do
       wget "http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_"$x"_"$y".zip"
   done
done
