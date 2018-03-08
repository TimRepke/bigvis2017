import networkx as nx
import argparse
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models.graphs import from_networkx
from os import listdir
from os.path import isfile, join
import re
import numpy as np
from datetime import datetime, timedelta

parser = argparse.ArgumentParser()
parser.add_argument('--nodes', type=int, default=100,
                    help='Number of nodes in the graph')
parser.add_argument('--cluster-size', dest='cluster_size', type=float, default=10.0,
                    help='Mean cluster size')
parser.add_argument('--cluster-size-variance', dest='cluster_size_variance', type=float, default=0.5,
                    help='Shape parameter. The variance of cluster size distribution is s/v.')
parser.add_argument('--intra', type=float, default=0.28,
                    help='Probabilty of intra cluster connection.')
parser.add_argument('--inter', type=float, default=0.004,
                    help='Probabilty of inter cluster connection.')
parser.add_argument('--directed', action='store_true',
                    help='Whether to create a directed graph or not (directed if set)')
parser.add_argument('--seed', type=int, default=42,
                    help='Seed value for random number generator')
parser.add_argument('--render', action='store_true',
                    help='Generate HTML page with graph visualisation')
parser.add_argument('--base-docs', dest='base_document_path', default='./base_documents/',
                    help='directory containing base documents')
parser.add_argument('--num-mails', dest='num_mails', type=int, default=2,
                    help='Mean number of emails from user A to user B')
parser.add_argument('--num-mails-variance', dest='num_mails_variance', type=float, default=50.0,
                    help='Variance to mean number of emails sent from user A to user B')
parser.add_argument('--topic-variance', dest='topic_variance', type=float, default=0.2,
                    help='Variance in topics a user writes about')
parser.add_argument('--mail-variance', dest='mail_variance', type=float, default=0.2,
                    help='Mean chance of dropping a word in an email.')
parser.add_argument('--max-mail-length', dest='max_mail_length', type=int, default=5000,
                    help='Maximum length of words per mail')
parser.add_argument('--from-time', dest='from_time', default='22/02/2016 11:15',
                    help='Earliest time an email was sent')
parser.add_argument('--to-time', dest='to_time', default='22/02/2017 20:15',
                    help='Latest time an email was sent')
parser.add_argument('--out-file', dest='out_file', default=None,
                    help='Set this parameter to write output to file')
args = parser.parse_args()

print(args)

np.random.seed(args.seed)

G = nx.generators.gaussian_random_partition_graph(n=args.nodes, s=args.cluster_size, v=args.cluster_size_variance,
                                                  p_in=args.intra, p_out=args.inter, directed=args.directed,
                                                  seed=args.seed)
if not args.directed:
    G = G.to_undirected()

if args.render:
    plot = figure(title="Networkx Integration Demonstration", x_range=(-1.1, 1.1), y_range=(-1.1, 1.1),
                  tools="", toolbar_location=None, width=1000, height=950)

    graph = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
    plot.renderers.append(graph)

    output_file("networkx_graph.html")
    show(plot)


def prepare_document(doc):
    return ' '.join([word for p_drop, word in zip(np.random.rand(args.max_mail_length),
                                                  doc[:args.max_mail_length]) if p_drop > args.mail_variance])


n_partitions = len(G.graph['partition'])

from_time = datetime.strptime(args.from_time, '%d/%m/%Y %H:%M')
to_time = datetime.strptime(args.to_time, '%d/%m/%Y %H:%M')
timeframe = (to_time - from_time) / timedelta(minutes=1)

base_document_filenames = [join(args.base_document_path, f)
                           for f in listdir(args.base_document_path) if isfile(join(args.base_document_path, f))]
base_documents = []
for f in listdir(args.base_document_path):
    if len(base_documents) >= n_partitions:
        break
    if isfile(join(args.base_document_path, f)) and f.endswith('.txt'):
        with open(join(args.base_document_path, f), 'r') as file:
            document = file.read()
            document = re.sub(r'\n', ' ', document)
            document = re.sub(r'\s+', ' ', document)
            base_documents.append(document.split())
n_documents = len(base_documents)

out_file = None
if args.out_file is not None:
    out_file = open(args.out_file, 'w')

for pi, partition in enumerate(G.graph['partition']):
    topic_distribution = [args.topic_variance / (n_documents - 1)] * n_documents
    topic_distribution[pi % n_documents] = 1.0 - args.topic_variance
    for node in partition:
        num_mails = np.abs(np.random.normal(args.num_mails, args.num_mails_variance, len(G.edges(node))).astype(int))
        for n_mails, edge in zip(num_mails, G.edges(node)):
            topics = np.random.choice(n_documents, size=n_mails, replace=True, p=topic_distribution)
            time_offsets = np.random.randint(0, int(timeframe), n_mails)
            for time_offset, topic in zip(time_offsets, topics):
                line = '{partition:d}\t{topic:d}\t{time:s}\t{sender:d}\t{recipient:d}\t{doc:s}' \
                       ''.format(partition=pi, topic=topic, sender=edge[0], recipient=edge[1],
                                 time=(from_time + timedelta(minutes=int(time_offset))).strftime('%d/%m/%Y %H:%M'),
                                 doc=prepare_document(base_documents[topic]))
                if out_file is None:
                    print(line)
                else:
                    out_file.write(line + '\n')
