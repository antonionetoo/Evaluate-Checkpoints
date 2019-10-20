from loadfromcheckpoints import LoadFromCheckpoint
from phraseconstructor import *
import argparse
from helptxt import *
from helpjson import load_json
from buildpredictions import *

def create_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-evaluate_checkpoint')
    parser.add_argument('-data_train')
    parser.add_argument('-data_ln_amr_anon')
    parser.add_argument('-type_evaluation')
    parser.add_argument('-output_predictions')
    parser.add_argument('-output_references')
    
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

def save_predicts_and_references_anon(data, name_predictions, name_references, type_evaluation):
    references_anon  = []
    predictions_anon = []
    first_type = type_evaluation.split('_')[0]

    for d in data:
        for region in d['regions']:
            if not region['phrase']['amr']['amr_anon_pred']:
                break
            
            predictions_anon.append(region['phrase'][first_type][type_evaluation + '_pred'] + '\n')
            references_anon.append( region['phrase'][first_type][type_evaluation + '_ref']  + '\n')

    save_txt(name_predictions, predictions_anon)
    save_txt(name_references, references_anon)

args = create_arguments()

constructor = PhraseConstructor()

data_ln_amr_anon   = obtain_phrases(load_json(args.data_ln_amr_anon))
data               = load_json(args.data_train)

data = constructor.construct_phrases(data, data_ln_amr_anon, args.type_evaluation)

loader = LoadFromCheckpoint()
references_predtions = loader.obtain_predict_and_reference(load_txt(args.evaluate_checkpoint))

builder = BuilderPredictions()
builder.build_predictions(references_predtions, data, args.type_evaluation)

save_predicts_and_references_anon(data, args.output_predictions, args.output_references, args.type_evaluation)

#python amr_simplifier/anonymized.py ../neural-graph-to-seq-mp/amr_ref_anon.txt
#mv amr_full.txt amr_anon_ref_full.txt
##########
#python anonymized.py ../neural-graph-to-seq-mp/amr_predict_anon.txt
#mv amr_full.txt amr_anon_pred_full.txt
