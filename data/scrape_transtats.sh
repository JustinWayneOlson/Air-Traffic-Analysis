#!/bin/sh
#years=(2016 2015 2014 2013 2012 2011 2010 2009 2008 2007 2006 2005 2004 2003 2002 2001 2000 1999 1998 1997 1996 1995 1994 1993 1992 1991 1990 1989 1988 1987)
years=(1989 1988 1987)
months=(1 2 3 4 5 6 7 8 9 10 11 12)

for x in ${years[*]}
do
   for y in ${months[*]}
   do
       wget "http://tsdata.bts.gov/PREZIP/On_Time_On_Time_Performance_"$x"_"$y".zip"
   done
done
