# cordis-scripts
Scripts to parse EU Open Data portal CSV files

First can download the CORDIS - EU research projects under Horizon 2020 (2014-2020) CSV file from http://cordis.europa.eu/data/cordis-h2020projects.csv

## Extracting all programmes and topics

    cordis_programmes_topics.py --input h2020projects.csv

This will create two file `programmes.txt` and `topics.txt` containing the corresponding fields extracted.

## Filtering projects based on topics

    cordis_filter_topics.py --input cordis-h2020projects.csv --topics_file topics.txt

This will read from text file `topics.txt` the list of topics that you want to include in the output and produce the filtering result in `output.csv`.


