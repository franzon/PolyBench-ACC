# Esse script somente executa o experimento para o construtor taskloop.

#!/bin/bash

benchmark=trmm
PREFIX_BENCHMARK=openmp
EXPERIMENT=taskloop

echo "Executing test for $benchmark, start at `date +'%d/%m/%Y-%T'`"

# Tamanhos dos dados considerados pelos benchmarks.
# TOY_DATASET MINI_DATASET TINY_DATASET SMALL_DATASET MEDIUM_DATASET STANDARD_DATASET 
# LARGE_DATASET EXTRALARGE_DATASET HUGE_DATASET 
for size_of_data in MINI_DATASET SMALL_DATASET STANDARD_DATASET LARGE_DATASET EXTRALARGE_DATASET; do
	for num_threads in 1 2 4 8 16; do
    echo "Compiling ${benchmark} with dataset: ${size_of_data}, threads: ${num_threads}."
    if [ -f "data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv" ]
    then
      echo "File: data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv [OK]"
      cat data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv >> ${benchmark}-joined-results.csv
    else
      echo "data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv [NOT FOUND]"
    fi
  done
done
echo "End of tests at `date +'%d/%m/%Y-%T'`"