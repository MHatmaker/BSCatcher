# !/usr/bin/bash

echo "Podcast catcher ready to catch some Bloomberg podcasts"

launchdir=/home/htmkr/Documents/Development/PythonProjects/Bloomberg/

cd $launchdir
pwd

/usr/bin/python CatchPodcasts.py
$SHELL

nautilus --browser ~/BloombergPodcasts
