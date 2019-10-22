#!/usr/bin/python

import sys
from nlgeval import NLGEval
from collections import OrderedDict
import pandas as pd

class EvaluateNL():
    def __init__(self):
        self.eval = NLGEval(no_skipthoughts=True, no_glove = True, 
            metrics_to_omit=['EmbeddingAverageCosineSimilairty', 'VectorExtremaCosineSimilarity', 'GreedyMatchingScore'])
        self._df = None
        self._metris = None

    @property
    def df(self):
        return self._df

    def compute(self, refs, hyps):
        data = []
        for i, ref in enumerate(refs):
            hyp = hyps[i]

            scores = self.eval.compute_individual_metrics(ref = [ref.replace('\n', '')], hyp = hyp.replace('\n', ''))
            scores = sorted(scores.items())
            self._metrics = [s[0] for s in scores]

            #data.append([ref, hyp])
            data.append([ref, hyp, *[float('%0.6f'%(s[1])) for s in scores]])

        return pd.DataFrame(data, columns = ['Reference', 'Hypotesi', *self._metrics])
        #self._df = pd.DataFrame(data, columns = ['Reference', 'Hypotesi', *self._metrics])
    
    def mean(self):
        avg = OrderedDict()
        for m in self._metrics:
            avg[m] = float('%0.6f'%(self._df.loc[:, m].mean()) )
        
        return avg
        