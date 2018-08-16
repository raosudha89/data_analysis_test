#!/bin/bash

SCRIPT_DIR=src
DATA_DIR=data

python $SCRIPT_DIR/main.py 	--data_csv_filename $DATA_DIR/rna002_RTRS_2013_06.csv \
				--tf_idf True \
				#--topic_modeling True \
				#--headlines_only True \

