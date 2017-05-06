A* Flight Time Estimation Using MLP Classifiers
============================
Language: Python 3.5

## Important Files
- MLP_Class.py - Class constructor for implementing MLP Classifier
- MLP Multi Month Tester.py - Tests multiple configurations of MLP Classifiers over multiple months
- cassandra_ml_init.py - Creates a table in Cassandra for MLP Class to store created classifiers
- MLP_Cassandra_Init_Fill.py - Fill Cassandra with common ML models for use in A*

## Usage
MLP_Class.py - Main function contains examples of usage with both csv files and Cassandra

MLP Multi Month Tester.py - csv_inputs is the list of Transtats csv files to read in, mlp_configs is a list of lists, with each list being configuration settings for the MLP classifier. Format of configurations is [alpha, (hlayer,hlayer,...,)]

cassandra_ml_init.py - Run this script on a machine running Cassandra, will attempt to connect to Cassandra and create a keyspace and table for storing trained MLP models

MLP_Cassandra_Init_Fill.py - Run this script to automatically fill Cassandra with common MLP models for use in A*
