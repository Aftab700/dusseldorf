#!/bin/bash

# This command connects locally and will probably work for you
mongodump --db=dusseldorf --out=./mongodb_backup

#
# This command uses a username and password to connect to a server
mongodump --db=dusseldorf --out=./mongodb_backup --username=admin --password=1cbf6ba177593ae0a1452642
