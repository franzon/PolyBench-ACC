import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


""" Gráficos """
""" 

    - Todas as combinações de schedule x chunk_size (grid) (para cada dataset)
    - Gráfico para cada combinação de dataset (fixar schedule e chunk)

 """
def generate_plot(title, sequencial_data, for_data, taskloop_data):
    sequencial_x, sequencial_error = sequencial_data
    for_x, for_error = for_data
    taskloop_x, taskloop_error = taskloop_data

    labels = ['1', '2', '4', '8', '16']

    x = np.arange(len(labels)) + 1

    width = 0.3

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, for_x, width, label='for', yerr=for_error,  align='center', alpha=0.8, ecolor='black', capsize=4,)
    rects2 = ax.bar(x + width/2, taskloop_x, width, label='taskloop', yerr=taskloop_error,  align='center', alpha=0.8, ecolor='black', capsize=4,)
    rects3 = ax.bar(0, sequencial_x, width, label='sequencial', yerr=sequencial_error,  align='center', alpha=0.8, ecolor='black', capsize=4,)

    ax.set_title(title)
    ax.set_xlabel('Numero de threads')
    ax.set_ylabel('Tempo (s)')
    ax.set_xticks(np.append([0], x))
    ax.set_xticklabels(['Sequencial'] + labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig('graficos/{}'.format(title))
    plt.close()



def dataset_thread_tempo():
    data_sequencial = pd.read_csv('trmm-joined-results-processed-final-sequencial.csv')
    data_for = pd.read_csv('trmm-joined-results-processed-final-for.csv')
    data_taskloop = pd.read_csv('trmm-joined-results-processed-final-taskloop.csv')

    executions_sequencial = data_sequencial.groupby(['size_of_data'])
    executions_sequencial = (executions_sequencial['OMP'].agg([np.mean, np.std]) / 1e9).reset_index()

    executions_for = data_for.groupby(['size_of_data', 'schedule', 'chunk_size', 'num_threads'])
    executions_for = (executions_for['OMP'].agg([np.mean, np.std]) / 1e9).reset_index()

    execution_taskloop = data_taskloop.groupby(['size_of_data', 'num_threads'])
    execution_taskloop = (execution_taskloop['OMP'].agg([np.mean, np.std]) / 1e9).reset_index()

    group_by_dataset =  executions_for.groupby(['size_of_data'])

    for dataset_name, dataset in group_by_dataset:
        sequencial = executions_sequencial[executions_sequencial['size_of_data'] == dataset_name]
        taskloop = execution_taskloop[execution_taskloop['size_of_data'] == dataset_name]

        global_min_time = 9999999999
        global_min_schedule_chunk = None
        global_min_schedule_chunk_name = None

        for schedule_chunk_name, schedule_chunk in dataset.groupby(['schedule', 'chunk_size']):
            schedule_chunk = schedule_chunk.sort_values('num_threads')

            concat = pd.concat([sequencial, taskloop, schedule_chunk], ignore_index=True)

            print(dataset_name, concat['mean'].min(), schedule_chunk_name )
            if concat['mean'].min() < global_min_time:
                global_min_time = concat['mean'].min()
                global_min_schedule_chunk = schedule_chunk
                global_min_schedule_chunk_name = schedule_chunk_name


        title = '{}-{}-{}'.format(dataset_name,  *global_min_schedule_chunk_name)            
        generate_plot(title, (sequencial['mean'], sequencial['std']), (global_min_schedule_chunk['mean'], global_min_schedule_chunk['std']), (taskloop['mean'], taskloop['std'])) 

            # plt.title(title)
            # plt.xlabel('Numero de threads')
            # plt.ylabel('Tempo (segundos)')

            # x = ['Sequencial', '1', '2', '4', '8', '16']
            # y = schedule_chunk['mean']
            # e = schedule_chunk['std']

            # plt.bar(x, y, yerr=e, align='center', alpha=0.5, ecolor='black', capsize=10, width=.5)
            # plt.savefig('graficos/{}'.format(title))
            # plt.close()

   

dataset_thread_tempo()
# generate_plot('teste', ([50], [20]), ([20, 34, 30, 35, 27], [1,2,3,4,5]),([25, 32, 34, 20, 25], [10,9,8,7,6]) )

# 

