# coding=utf-8

from loadfromcheckpoints import LoadFromCheckpoint
from phraseconstructor import *
import argparse
from parser_anon_to_ln import ParserAnonToNl
from helpjson import *
from helptxt import *
from buildpredictions import *
import pandas as pd
import os
from evaluateamr import EvaluateAMR

def create_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-evaluate_checkpoint')
    parser.add_argument('-data_train')
    parser.add_argument('-data_ln_amr_anon')
    parser.add_argument('-type_evaluation')
    parser.add_argument('-data_ln')
    
    return parser.parse_args()

def obtain_phrases(data):
    phrases_ln   = []
    phrases_anon = []
    phrases_amr  = []
    for k, v in data.items():
        phrases_ln.append(k)
        phrases_amr.append(v[0])
        phrases_anon.append(v[1])
    
    return {'ln':phrases_ln, 'anon':phrases_anon, 'amr':phrases_amr}  

def get_phrase(data, type1, type2, end = '\n'):
    result = []

    for d in data:
        for region in d['regions']:    
            result.append(region['phrase'][type1][type2] + end)

    return result

def save_csv(data):
    data_csv = []
    for d in data:
        for i, region in enumerate(d['regions']):
            if not region['phrase']['ln']['ln_pred']:
                break
            
            data_csv.append(['{}-{}'.format(d['id'],i), 
                        region['phrase']['ln']['ln_ref'], 
                        region['phrase']['amr']['amr_full_ref'], 
                        region['phrase']['amr']['amr_anon_ref'],
                        region['phrase']['ln']['ln_ref_anon'],
                        region['phrase']['amr']['amr_anon_ref_full'],
                        region['phrase']['amr']['amr_anon_pred'],
                        region['phrase']['ln']['ln_pred'],
                        region['phrase']['amr']['amr_anon_pred_full']])
                    
    df = pd.DataFrame(data_csv, columns = ['Chave', 'Referência LN', 'Referência AMR', 'Referência Anon', 'Predita LN Referência Anon', 
                                        'Referência Anon Transformada em full', 'Predita Anon', 'Predita LN', 'Predita Anon Transformada em full'])                

    df.to_csv('saida.csv')

def evaluate(data, type):
    save_txt('ln_refs.txt', get_phrase(data, 'ln', 'ln_ref'))
    save_txt('ln_preds.txt', get_phrase(data, 'ln', 'ln_pred'))
    save_txt('ln_refs_anon.txt', get_phrase(data, 'ln', 'ln_ref_anon'))

    os.system('python3 evaluatenl.py -refs ln_refs.txt -pred ln_preds.txt -refs_anon ln_refs_anon.txt -type_evaluation {}'.format(type))

    if not type == 'ln':
        
        #ids = [i for i, a in enumerate(amr_anon_pred_full) if not a.startswith('FAILED')]
        ids = []

        amr_full_ref       = get_phrase(data, 'amr', 'amr_full_ref', '\n\n')

        amr_anon_ref_full  = get_phrase(data, 'amr', 'amr_anon_ref_full', '\n\n')
        ids = [i for i, d in enumerate(amr_anon_ref_full) if d.startswith('FAILED')]

        amr_anon_pred_full = get_phrase(data, 'amr', 'amr_anon_pred_full', '\n\n')
        ids =  ids + [i for i, d in enumerate(amr_anon_pred_full) if d.startswith('FAILED')]

        # ids.append(174)
        # ids.append(177)
        
        eval_amr = EvaluateAMR()
        eval_amr.evaluate([d for i, d in enumerate(amr_full_ref) if i not in ids],
                          [d for i, d in enumerate(amr_anon_ref_full) if i not in ids], 
                          [d for i, d in enumerate(amr_anon_pred_full) if i not in ids]
                          )   

args = create_arguments()

data_ln_amr_anon = load_json(args.data_ln_amr_anon)
data             = load_json(args.data_train)

constructor = PhraseConstructor()
data = constructor.construct_phrases(data, 
                                    load_json(args.data_ln), 
                                    data_ln_amr_anon,
                                    args.type_evaluation)

loader = LoadFromCheckpoint()
references_predtions = loader.obtain_predict_and_reference(load_txt(args.evaluate_checkpoint))

builder = BuilderPredictions()
data = builder.build_predictions(references_predtions, data, args.type_evaluation)

parser_anon_nl = ParserAnonToNl(data)
parser_anon_nl.parse(args.type_evaluation)

evaluate(parser_anon_nl.data, args.type_evaluation)

save_csv(parser_anon_nl.data)

save_json('data.json', parser_anon_nl.data)
