#!/bin/bash -xe

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <benchmark>" >&2
  exit 1
fi

benchmark=$1

for result_file in `ls ${benchmark}-joined-results.csv | cut -d'/' -f2`; do
	echo "csvizing ${result_file}"
	result_file_name=${result_file%.csv}
	./csvize-experiments-results.py -i ${result_file} -o ${result_file_name}-processed.csv

  cp ${result_file_name}-processed.csv ${result_file_name}-processed-final.csv
done