import pandas as pd
import numpy as np
import gensim
import os
import collections
import random


def read_corpus(frame, tokens_only=False):
    for i, (_, line) in enumerate(frame.iterrows()):
        try:
            if tokens_only:
                yield gensim.utils.simple_preprocess(line['body'])
            else:
                # For training data, add tags
                yield gensim.models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line['body']), [i])
        except TypeError:
            pass


if __name__ == '__main__':
    dimensions = 50
    df = pd.read_csv('emails.csv', escapechar='\\')
    corpus = list(read_corpus(df))

    model = gensim.models.doc2vec.Doc2Vec(size=dimensions, min_count=2, iter=55)
    model.build_vocab(corpus)

    print('training!')
    model.train(corpus, total_examples=model.corpus_count, epochs=model.iter)
    print('done')

    print('inferring!')
    dicts = df.to_dict(orient='records')
    for dic in dicts:
        try:
            vec = model.infer_vector(gensim.utils.simple_preprocess(dic['body']))
        except TypeError:
            vec = np.ones((dimensions,))
        dic['vec'] = vec

    pd.DataFrame(dicts).to_csv('emails.emb.csv', escapechar='\\', index=False)
    print('done and saved!')
    # ranks = []
    # second_ranks = []
    # for doc_id in range(len(corpus)):
    #     inferred_vector = model.infer_vector(corpus[doc_id].words)
    #     sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
    #     rank = [docid for docid, sim in sims].index(doc_id)
    #     ranks.append(rank)
    #
    #     second_ranks.append(sims[1])

    # print(collections.Counter(ranks))

    # doc_id = random.randint(0, len(corpus))
    # print('Document ({}): «{}»\n'.format(doc_id, ' '.join(corpus[doc_id].words)))
    # print(u'SIMILAR/DISSIMILAR DOCS PER MODEL %s:\n' % model)
    # for label, index in [('MOST', 0), ('MEDIAN', len(sims) // 2), ('LEAST', len(sims) - 1)]:
    #     print(u'%s %s: «%s»\n' % (label, sims[index], ' '.join(corpus[sims[index][0]].words)))
    #
    # # Compare and print the most/median/least similar documents from the train corpus
    # print('Train Document ({}): «{}»\n'.format(doc_id, ' '.join(corpus[doc_id].words)))
    # sim_id = second_ranks[doc_id]
    # print('Similar Document {}: «{}»\n'.format(sim_id, ' '.join(corpus[sim_id[0]].words)))
