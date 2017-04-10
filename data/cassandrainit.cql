/* ---------------------------------------------------------------------
Author: Michael Muehlbradt
Contributor: Mitch Zinser
This script creates keyspace and tables for db setup
DBSchema: table for transtats and ADSBExchange
Table naming convention: 
Usage: run this command in cqlsh: SOURCE 'path-to-/cassandra_setup.cql'
-------------------------------------------------------------------------
*/
CREATE KEYSPACE IF NOT EXISTS AirportTrafficAnalytics WITH replication = { 'class' : 'SimpleStrategy',
'replication_factor' : '2' } AND durable_writes = true;

USE AirportTrafficAnalytics;


/* ------------------------------------------------------------
Tables for Transtats
------------------------------------------------------------ */
CREATE TABLE Transtats (
"Year" bigint, //formerly timestamp
"Quarter" bigint,
"Month" bigint,
"DayofMonth" bigint,
"DayOfWeek" bigint,
"FlightDate" timestamp, //formerly text 
"UniqueCarrier" text,
"AirlineID" bigint,
"Carrier" text,
"TailNum" text,
"FlightNum" bigint,
"OriginAirportID" bigint,
"OriginAirportSeqID" bigint,
"OriginCityMarketID" bigint,
"Origin" text,
"OriginCityName" text,
"OriginState" text,
"OriginStateFips" bigint,
"OriginStateName" text,
"OriginWac" bigint,
"DestAirportID" bigint,
"DestAirportSeqID" bigint,
"DestCityMarketID" bigint,
"Dest" text,
"DestCityName" text,
"DestState" text,
"DestStateFips" bigint,
"DestStateName" text,
"DestWac" bigint,
"CRSDepTime" bigint,
"DepTime" double,
"DepDelay" double,
"DepDelayMinutes" double,
"DepDel15" double,
"DepartureDelayGroups" double,
"DepTimeBlk" text,
"TaxiOut" double,
"WheelsOff" double,
"WheelsOn" double,
"TaxiIn" double,
"CRSArrTime" bigint,
"ArrTime" double,
"ArrDelay" double,
"ArrDelayMinutes" double,
"ArrDel15" double,
"ArrivalDelayGroups" double,
"ArrTimeBlk" text,
"Cancelled" double,
"CancellationCode" text,
"Diverted" double,
"CRSElapsedTime" double,
"ActualElapsedTime" double,
"AirTime" double,
"Flights" double,
"Distance" double,
"DistanceGroup" bigint,
"CarrierDelay" double,
"WeatherDelay" double,
"NASDelay" double,
"SecurityDelay" double,
"LateAircraftDelay" double,
"FirstDepTime" double,
"TotalAddGTime" double,
"LongestAddGTime" double,
"DivAirportLandings" bigint,
"DivReachedDest" double,
"DivActualElapsedTime" double,
"DivArrDelay" double,
"DivDistance" double,
"Div1Airport" text,
"Div1AirportID" double,
"Div1AirportSeqID" double,
"Div1WheelsOn" double,
"Div1TotalGTime" double,
"Div1LongestGTime" double,
"Div1WheelsOff" double,
"Div1TailNum" text,
"Div2Airport" text,
"Div2AirportID" double,
"Div2AirportSeqID" double,
"Div2WheelsOn" double,
"Div2TotalGTime" double,
"Div2LongestGTime" double,
"Div2WheelsOff" double,
"Div2TailNum" text,
"Div3Airport" text,
"Div3AirportID" double,
"Div3AirportSeqID" double,
"Div3WheelsOn" double,
"Div3TotalGTime" double,
"Div3LongestGTime" double,
"Div3WheelsOff" double,
"Div3TailNum" text,
"Div4Airport" text,
"Div4AirportID" double,
"Div4AirportSeqID" double,
"Div4WheelsOn" double,
"Div4TotalGTime" double,
"Div4LongestGTime" double,
"Div4WheelsOff" double,
"Div4TailNum" text,
"Div5Airport" text,
"Div5AirportID" double,
"Div5AirportSeqID" double,
"Div5WheelsOn" double,
"Div5TotalGTime" double,
"Div5LongestGTime" double,
"Div5WheelsOff" double,
"Div5TailNum" text,
"Unnamed: 109" double,
PRIMARY KEY ("FlightNum", "FlightDate"),
) WITH CLUSTERING ORDER BY ("FlightDate" DESC);

/*End Transtats Table*/

/*--------------------------------------------------------
Tables for Routing
--------------------------------------------------------- */
CREATE TYPE Node ("lat" double, "long" double, "alt" double, "speed" double, "time" timestamp);
CREATE TYPE Coord ("lat" double, "long" double);
CREATE TYPE Links ("source" double, "target" double);

CREATE TABLE Routing (
"jobNum" int,
"jobName" text,                               
"Carrier" text,
"DepTime" double,
"FlightNum" bigint,
"FlightDate" timestamp, //formerly text
"Origin" text,
"Dest" text,
"gridResPlanar" int,
"gridResVert" int,                
"gridLines" map <frozen <Coord>, frozen <Links>>,
"routeLines" map <frozen <Node>, frozen <Links>>,
PRIMARY KEY ("FlightNum", "FlightDate"),
) WITH CLUSTERING ORDER BY ("FlightDate" DESC);

/* --------------------------------------------------------
Tables for MLPClassifier
---------------------------------------------------------- */
CREATE TABLE MLPClassifier (
   "Year" bigint,
   "Month" bigint,
   "RoundingBase" bigint,
   "Features" text,
   "Label" text,
   "HLayer" text,
   "Alpha" double,
   "RowsTrain" bigint,
   "Accuracy" double,
   "Model" text,
   PRIMARY KEY ("Year", "Month", "RoundingBase", "Features", "Label", "HLayer", "Alpha"),
  ); // WITH CLUSTERING ORDER BY ("Month" DESC, "RoundingBase" DESC, "Year" DESC);

                
/* --------------------------------------------------------
Tables for AirpotLocations
---------------------------------------------------------- */
CREATE TABLE AirportLocations (
   "City" text,
   "Code" text,
   "Lat" double,
   "Lon" double,
   "alt" double,

   PRIMARY KEY ("Code"),
  );

