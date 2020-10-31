# Esse script somente executa o experimento sequencialmente.

#!/bin/bash

benchmark=trmm
PREFIX_BENCHMARK=openmp
EXPERIMENT=sequencial

echo "Executing test for $benchmark, start at `date +'%d/%m/%Y-%T'`"

# Tamanhos dos dados considerados pelos benchmarks.
# TOY_DATASET MINI_DATASET TINY_DATASET SMALL_DATASET MEDIUM_DATASET STANDARD_DATASET 
# LARGE_DATASET EXTRALARGE_DATASET HUGE_DATASET 
for size_of_data in MINI_DATASET SMALL_DATASET STANDARD_DATASET LARGE_DATASET EXTRALARGE_DATASET; do
		echo "Compiling ${benchmark} with dataset: ${size_of_data}."
		if [ -f "data-${benchmark}-dataset-${size_of_data}-${PREFIX_BENCHMARK}.csv" ]
        then
          echo "File: data-${benchmark}-dataset-${size_of_data}-${PREFIX_BENCHMARK}.csv [OK]"
          cat data-${benchmark}-dataset-${size_of_data}-${PREFIX_BENCHMARK}.csv >> ${benchmark}-joined-results.csv
        else
          echo "data-${benchmark}-dataset-${size_of_data}-${PREFIX_BENCHMARK}.csv [NOT FOUND]"
        fi
done
echo "End of tests at `date +'%d/%m/%Y-%T'`"
