import sys

import matplotlib.pyplot as plt
import networkx as nx
import json
import pandas as pd
import flask
from networkx.readwrite import json_graph

if __name__ == '__main__':
    df = pd.read_csv('emails.csv', escapechar='\\')
    rows = df.to_dict(orient='records')
    G = nx.Graph()

    for row in rows:
        if G.has_edge(row['from'], row['to']):
            G[row['from']][row['to']]['value'] += 1
        else:
            G.add_edge(row['from'], row['to'], value=1)

    # G = nx.read_graphml('graph.graphml')#.to_undirected()
    # G = nx.barbell_graph(6, 3)
    # this d3 example uses the name attribute for the mouse-hover value,
    # so add a name to each node
    for n in G:
        G.nodes[n]['name'] = n
    #for e in G.edges:
    #    G[e[0]][e[1]]['value'] = G[e[0]][e[1]]['weight']

    # write json formatted data
    d = json_graph.node_link_data(G)  # node-link format to serialize
    # write json
    json.dump(d, open('force/force.json', 'w'))
    print('Wrote node-link JSON data to force/force.json')

    # Serve the file over http to allow for cross origin requests
    app = flask.Flask(__name__, static_folder="force")


    @app.route('/<path:path>')
    def static_proxy(path):
        return app.send_static_file(path)


    print('\nGo to http://localhost:8000/force.html to see the example\n')
    app.run(port=8000)
