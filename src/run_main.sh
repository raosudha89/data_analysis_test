#!/bin/bash

SCRIPT_DIR=src
DATA_DIR=data

python $SCRIPT_DIR/main.py 	--data_csv_filename $DATA_DIR/rna002_RTRS_2013_06.csv \
				--topic_modeling True \
				#--topic_modeling_per_topic True \
				#--collocations True \
				#--tf_idf True \
				#--headlines_only True \

