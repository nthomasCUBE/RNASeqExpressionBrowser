#!/usr/bin/bash

# --------------------------------------

# Gene ontology analysis

cd go
unzip gene_ontology.1_2.zip
cd ..

# --------------------------------------

cd example/barley/
unzip transcripts_NT.zip
cd ../..

# --------------------------------------

python installation.py installation_example.conf






