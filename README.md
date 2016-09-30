Air Traffic Analysis Project 
============================
University of Colorado and Northrop Grumman

Justin Olson, Michael Muehlbradt, Kristen Hanslik, Mitch Zinser, and Matt Oakley

## Requirements
 * [Git](http://git-scm.com/)
 * [Python (2.7)](http://python.org/)
 * [Python Tornado](http://www.tornadoweb.org/en/stable/)
 * [PostgreSQL](https://www.postgresql.org/)
 * [Python Psycopg2](http://initd.org/psycopg/docs/) 

##File structure
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
