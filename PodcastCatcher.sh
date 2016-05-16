# !/usr/bin/bash

echo "Podcast catcher ready to catch some Bloomberg podcasts"

launchdir=/home/htmkr/Development/PythonProjects/Bloomberg/

cd $launchdir
pwd

/usr/bin/python DownloadXml.py
