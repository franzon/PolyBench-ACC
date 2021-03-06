import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os

def prepare_folders():
    shutil.rmtree('graficos')

    os.mkdir('graficos')
    os.mkdir('graficos/thread')
    os.mkdir('graficos/schedule')
    os.mkdir('graficos/chunk')


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
    ax.set_xlabel('Número de threads')
    ax.set_ylabel('Tempo (s)')
    ax.set_xticks(np.append([0], x))
    ax.set_xticklabels(['Sequencial'] + labels)
    ax.legend()

    fig.tight_layout()

    plt.savefig('graficos/thread/{}'.format(title))
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

            if concat['mean'].min() < global_min_time:
                global_min_time = concat['mean'].min()
                global_min_schedule_chunk = schedule_chunk
                global_min_schedule_chunk_name = schedule_chunk_name

        time_sequencial = sequencial.iloc[0]['mean']
        times_for = [row['mean'] for i, row in global_min_schedule_chunk.iterrows()]
        times_taskloop = [row['mean'] for i, row in taskloop.iterrows()]

        print('Speedup results [{}]'.format(dataset_name))
        print('For: {}'.format([round(time_sequencial / x, 2)  for x in times_for]))
        print('Taskloop: {}'.format([round(time_sequencial / x, 2) for x in times_taskloop]))
        print('\n')

        title = '{}-{}-{}'.format(dataset_name,  *global_min_schedule_chunk_name)            
        generate_plot(title, (sequencial['mean'], sequencial['std']), (global_min_schedule_chunk['mean'], global_min_schedule_chunk['std']), (taskloop['mean'], taskloop['std'])) 

prepare_folders()
dataset_thread_tempo()