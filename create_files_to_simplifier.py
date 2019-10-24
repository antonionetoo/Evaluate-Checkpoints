# coding=utf-8

from loadfromcheckpoints import LoadFromCheckpoint
from phraseconstructor import *
import argparse
from parser_anon_to_ln import ParserAnonToNl
from helpjson import load_json
from helptxt import *
from buildpredictions import *
import pandas as pd
import os

def create_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-evaluate_checkpoint')
    parser.add_argument('-data_train')
    parser.add_argument('-data_ln_amr_anon')
    parser.add_argument('-type_evaluation')
    
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

def save_csv(data):
    data_csv = []
    for d in data:
        for i, region in enumerate(d['regions']):
            if not region['phrase']['amr']['amr_anon_pred']:
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

args = create_arguments()

constructor = PhraseConstructor()

data_ln_amr_anon = obtain_phrases(load_json(args.data_ln_amr_anon))
data             = load_json(args.data_train)

data = constructor.construct_phrases(data, data_ln_amr_anon, args.type_evaluation)

loader = LoadFromCheckpoint()
references_predtions = loader.obtain_predict_and_reference(load_txt(args.evaluate_checkpoint))

builder = BuilderPredictions()
builder.build_predictions(references_predtions, data, args.type_evaluation)

parser_anon_nl = ParserAnonToNl(data)
parser_anon_nl.parse(args.type_evaluation)


ln_preds     = []
ln_refs      = []
ln_refs_anon = []

for d in parser_anon_nl.data:
    for region in d['regions']:
            if not region['phrase']['amr']['amr_anon_pred']:
                break

            ln_refs.append(region['phrase']['ln']['ln_ref'] + '\n')
            ln_preds.append(region['phrase']['ln']['ln_pred'] + '\n')
            ln_refs_anon.append(region['phrase']['ln']['ln_ref_anon'] + '\n')

save_txt('ln_refs.txt', ln_refs)
save_txt('ln_preds.txt', ln_preds)
save_txt('ln_refs_anon.txt', ln_refs_anon)

os.system('python3 evaluatenl.py -refs ln_refs.txt -pred ln_preds.txt -refs_anon ln_refs_anon.txt')
#eval = load_json('eval.json')



save_csv(parser_anon_nl.data)


#python src_g2s/G2S_beam_decoder.py --model_prefix logs_g2s/G2S.silver_2m --in_path test_ref.json --out_path ln_ref.parsed --mode beam
#python src_g2s/G2S_beam_decoder.py --model_prefix logs_g2s/G2S.silver_2m --in_path test_pred.json --out_path ln_pred.parsed --mode beam

#export CUDA_VISIBLE_DEVICES=0


#python amr_simplifier/anonymized.py ../neural-graph-to-seq-mp/amr_ref_anon.txt
#mv amr_full.txt amr_anon_ref_full.txt
##########
#python anonymized.py ../neural-graph-to-seq-mp/amr_predict_anon.txt
#mv amr_full.txt amr_anon_pred_full.txt
