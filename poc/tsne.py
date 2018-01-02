import numpy as np
import pandas as pd
from sklearn.manifold import TSNE

df = pd.read_csv('emails.emb.csv', escapechar='\\')

vectors = np.array([np.fromstring(v[1:-1], sep=' ') for v in list(df['vec'])])
print('loaded!', vectors.shape)
print('fitting now')
embedded = TSNE(n_components=2, verbose=1).fit_transform(vectors)

print('fitted.')
rows = df.to_dict(orient='records')
for row, emb in zip(rows, embedded):
    row['2d'] = emb

pd.DataFrame(rows).to_csv('emails.emb2d.csv', escapechar='\\', index=False)
print('saved.')
