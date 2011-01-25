#!/bin/sh

# Change to the kml_generator folder
cd /path/to/kml_generator

# Leave this be
python generate_kml.py

# Change second part to the www/kml folder
cp kml/*.kml /path/to/kml
