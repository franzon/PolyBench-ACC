import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

csv_files = [
    'trmm-joined-results-processed-final-for.csv',
    'trmm-joined-results-processed-final-sequencial.csv',
    # TODO: taskloop
]

lines = []

for file_name in csv_files:
    df = pd.read_csv(file_name, index_col=None, header=0)
    lines.append(df)

data = pd.concat(lines, axis=0, ignore_index=True)

data_for = data[data['exp'] == 'for']
data_sequencial = data[data['exp'] == 'sequencial']

print(data_for)
print(data_sequencial)

# executions = data_for.groupby(['size_of_data', 'schedule', 'chunk_size', 'num_threads'])
# executions = (executions['OMP'].agg([np.mean, np.std]) / 1e9)

# graphs_data = executions.groupby(['size_of_data', 'schedule', 'chunk_size'])

# for names, graph in graphs_data:
#     title = 'Dataset: {}  Schedule: {}    Chunk size: {}'.format(*names)

#     plt.title(title)
#     plt.xlabel('Numero de threads')
#     plt.ylabel('Tempo (segundos)')

#     x = ['1', '2', '4', '8', '16']
#     y = graph['mean']
#     e = graph['std']

#     plt.bar(x, y, yerr=e,  align='center', alpha=0.5, ecolor='black', capsize=10, width=4)
#     plt.savefig('graficos/{}'.format(title))