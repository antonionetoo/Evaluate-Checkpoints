
import sys
import argparse
from nlgeval import NLGEval
import pandas as pd
from helptxt import load_txt
import csv

class EvaluateNL():
    def __init__(self):
        self.eval = NLGEval(no_skipthoughts=True, no_glove = True, 
            metrics_to_omit=['EmbeddingAverageCosineSimilairty', 'VectorExtremaCosineSimilarity', 'GreedyMatchingScore'])

    def compute(self, refs, hyps):
        data = []
        for i, ref in enumerate(refs):
            ref = ref.replace('\n', '')
            hyp = hyps[i].replace('\n', '')

            scores = self.eval.compute_individual_metrics(ref = [ref.replace('\n', '')], hyp = hyp.replace('\n', ''))
            scores = sorted(scores.items())
            self._metrics = [s[0] for s in scores]

            #data.append([ref, hyp])
            data.append([ref, hyp, *[str(float('%0.6f'%(s[1]))).replace('.',',') for s in scores]])

        return pd.DataFrame(data, columns = ['Reference', 'Hypotesi', *self._metrics])

def create_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-refs')
    parser.add_argument('-pred')
    parser.add_argument('-refs_anon')
    
    return parser.parse_args()

if __name__ == '__main__':

    args = create_arguments()

    refs = load_txt(args.refs)
    pred = load_txt(args.pred)
    refs_anon = load_txt(args.refs_anon)

    eval = EvaluateNL()

    df = eval.compute(refs, refs_anon)
    df.to_csv('eval_refs_anon.csv')
    df.to_json('eval_refs_anon.json')

    df  = eval.compute(refs, pred)
    df.to_csv('eval_refs_pred.csv')
    df.to_json('eval_refs_pred.json')

    df = eval.compute(refs_anon, pred)
    df.to_csv('eval_refs_anon_pred.csv')
    df.to_json('eval_refs_anon_pred.json')
