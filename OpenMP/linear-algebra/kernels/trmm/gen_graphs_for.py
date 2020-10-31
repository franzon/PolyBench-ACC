import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def main():
    data_for = pd.read_csv('trmm-joined-results-processed-final-for.csv')
    data_sequencial = pd.read_csv('trmm-joined-results-processed-final-sequencial.csv')

    executions_sequencial = data_sequencial.groupby(['size_of_data'])
    executions_sequencial = (executions_sequencial['OMP'].agg([np.mean, np.std]) / 1e9).reset_index()

    executions_for = data_for.groupby(['size_of_data', 'schedule', 'chunk_size', 'num_threads'])
    executions_for = (executions_for['OMP'].agg([np.mean, np.std]) / 1e9).reset_index()

    graphs_data = executions_for.groupby(['size_of_data', 'schedule', 'chunk_size'])

    for names, graph in graphs_data:

        sequencial = executions_sequencial[executions_sequencial['size_of_data'] == names[0]]
        sequencial.loc[:, 'num_threads'] = 0
        
        graph = graph.append(sequencial)
        graph = graph.sort_values('num_threads')
        
        title = '{}-{}-{}'.format(*names)

        plt.title(title)
        plt.xlabel('Numero de threads')
        plt.ylabel('Tempo (segundos)')

        x = ['Sequencial', '1', '2', '4', '8', '16']
        y = graph['mean']
        e = graph['std']

        plt.bar(x, y, yerr=e, align='center', alpha=0.5, ecolor='black', capsize=10, width=.5)
        plt.savefig('graficos/{}'.format(title))
        plt.close()

main()
