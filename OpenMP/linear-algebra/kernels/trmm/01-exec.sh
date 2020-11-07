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
		# make POLYBENCH_OPTIONS="-DPOLYBENCH_TIME -DTOY_DATASET" OMP_CONFIG="-DOPENMP_SCHEDULE_DYNAMIC -DOPENMP_CHUNK_SIZE=64 -DOPENMP_NUM_THREADS=24"
		make POLYBENCH_OPTIONS="-DPOLYBENCH_TIME -D${size_of_data}" OMP_CONFIG="-DOPENMP_NUM_THREADS=${num_threads}"
		mv ${benchmark}-${PREFIX_BENCHMARK}.exe ${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.exe
		for ((  i = 1 ;  i <= 10;  i++  ))
		do
			echo "Executing..."
			echo "Experiment '${EXPERIMENT}', execution ${i} of ${benchmark} with dataset: ${size_of_data}, threads: ${num_threads} start at `date +'%d/%m/%Y-%T'`"
			echo "Experiment '${EXPERIMENT}', execution ${i} of ${benchmark} with dataset: ${size_of_data}, threads: ${num_threads} start at `date +'%d/%m/%Y-%T'`" >> data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}-stderr.csv
			echo "exp = ${EXPERIMENT}, execution = ${i}, benchmark = ${benchmark}, size_of_data = ${size_of_data}, num_threads = ${num_threads}," >> data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv
			./${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.exe ${size_of_data} >> data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}.csv 2>> data-${benchmark}-dataset-${size_of_data}-threads-${num_threads}-${PREFIX_BENCHMARK}-stderr.csv
		done
	done
done
echo "End of tests at `date +'%d/%m/%Y-%T'`"