Waffle Project Tracking [![Stories in Ready](https://badge.waffle.io/JustinWayneOlson/Air-Traffic-Analysis.png?label=ready&title=Ready)](https://waffle.io/JustinWayneOlson/Air-Traffic-Analysis)
Air Traffic Analysis Project 
============================
University of Colorado and Northrop Grumman

Justin Olson, Michael Muehlbradt, Kristen Hanslik, Mitch Zinser, and Matt Oakley

Air Traffic Analysis is a full stack application, capable of ingesting and storing flight data, processing data and training neural networks, calculating efficient flight routes, displaying historic and calculated flights paths accurately on a map, and allowing interactive user input for requesting more flight paths. This project is extensible, documented, and open-source. Potential applications of this product include: research tool for displaying flight paths, analysis of current and potential flight path heuristics, or database integrated machine learning framework.



## Requirements
 * [Python (2.7)](http://python.org/)
 * [Python (3.5)](http://python.org/)
 * [PostgreSQL](https://www.postgresql.org/)
 * [Cassandra](http://cassandra.apache.org/)
 
## Python2 Libraries
 * [Python Tornado](http://www.tornadoweb.org/en/stable/)
 * [Python Psycopg2](http://initd.org/psycopg/docs/) 
 
## Python3 Libraries
 * [Numpy](http://www.numpy.org/)
 * [Scipy](https://www.scipy.org/)
 * [Scikit-Learn](http://scikit-learn.org/stable/)
 * [Cassandra-Driver](https://github.com/datastax/python-driver)

Full installation, setup, and running instructions can be found in the provided [White Paper](documentation/White_Paper.pdf)

## File structure
```
project
├── application
│   └── src
│       ├── app.py
│       ├── css
│       │   └── style.css
│       ├── html
│       │   └── index.html
│       ├── img
│       │   └── temp.jpg
│       └── js
│           └── index.js
├── data
│   ├── data_source.py
│   └── db_init.py
└── README.md

```

app.py - Python Tornado Server

style.css - stylesheet for the main page

index.html - main page

index.js - JavaScript for main page

data\_source.py - retrieve data, process, import to database

db\_init.py - creates empty database 

## Usage

###Install dependencies

PostgreSQL

https://www.postgresql.org/download/

Python Tornado

    pip install tornado

Psycopg2

    pip install psycopg2

Clone the project

    git clone https://github.com/JustinWayneOlson/Air-Traffic-Analysis

Create empty PSQL database

    python db_init.py

Pull data and fill PSQL database

    python data_source.py

Start Tornado server

    python app.py

Point browser to http://localhost:8888/index.html
