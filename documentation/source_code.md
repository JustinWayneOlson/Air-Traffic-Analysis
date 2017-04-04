# Source Code

## Application/src
* ### data
    * `airport_locs.csv`: City/Airport/Lat/Lon data
* ### html
    * `about.html`: About page
    * `index.html`: Home page
    * `routing.html`: Routing page
* ### img
    ...
* ### static
    * ##### css
        *  `jquery.datetimepicker.min.css`: CSS for JS date/time picker library
        *  `leaflet-openweathermap.css`: CSS for Leaflet library
        *  `style.css`: CSS for `about.html`
    * ##### img
        * `cu.png`: CU logo
        * `loading.gif`: Loading gif for query execution
        * `ng.png`: Northrop Grumman logo
    * ##### js
        * `index.js`: JS functions used in `about.html`
        ...
* `app.py`: Tornado server to handle requests
* `helpers.py`: Additional functions utilized in app.py

## Data
* ### Analysis/delay_prediction
    * `1585_combos_3_iters_range_1-6_200000_data.csv`: *
    * `2510_combos_3_iters_range_6-13_200000_data.csv`: *
    * `MLPClassifier.py`: *
    * `README.md`: *
    * `average_tester.py`: *
    * `classifier_comp.py`: *
    * `k_neigh_auto.py`: *
    * `test_learn.py`: *
    * `thread_feature_finder.py`: *
* ### Data
    * `airport_location_gen.py`: Transfer data from .dat file to .CSV
    * `airport_locations.csv`: City/Airport Code/Lat/Lon data
    * `airport_locations_dat`': City/Airport Code/Lat/Lon data
    * `airport_locations_out.csv`: City/Airport Code/Lat/Lon data [extended]
    * `data_downloader.py`: Downloads data from Transtats
    * `data_downloader_threaded.py`: Downloads data from Transtats synchronously
    * `readme.html`: Transtats table schema
* ### Vis
    * `plotly_vis_test.py`: Visualizes Transtats data using Plotly library


* `cassandra_fill.py`: Populates Cassandra database from CSV
* `cassandra_init.py`: Initializes database and table to store Transtats data
* `cassandrainit.cql`: Creates keyspace and tables for Cassandra database
* `data_extraction.py`: Processes Excel data and creates respective PostgreSQL table
* `data_source.py`: N/A
* `db_init.py`: Initializes PostgreSQL database
* `insertTranstats.cql`: Inserts NULL data into Cassandra database
* `scrape_stranstats.sh`: Downloads Transtats data (ZIP files)

## Documentation
* `Presentation2.pptx`: Team planning presentation
* `blah.txt`: N/A

## Routing
* `Routing.py`: *
* `RoutingOO.py`: *

## Testing
* `UnitTestSuite.py`: Unit testing suite

`.gitignore`: Removes version control from ZIP and TAR files
`README.md`: Basic project information
`notes.txt`: Team notes
