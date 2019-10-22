import os
import simplifier
from helptxt import load_txt
from helpjson import save_json

class ParserAnonToNl:
    def __init__(self, data):
        self.data = data

    def load_anon_full(self, anon_full):
        amr_anon_ref_full  = iter([a for a in anon_full[0] if a != '\n' ])
        amr_anon_pred_full = iter([a for a in anon_full[1] if a != '\n'])
        for d in self.data:
            for region in d['regions']:
                if region['phrase']['amr']['amr_anon_pred']:
                    region['phrase']['amr']['amr_anon_ref_full'] = next(amr_anon_ref_full).replace('\n', '')
                    region['phrase']['amr']['amr_anon_pred_full'] = next(amr_anon_pred_full).replace('\n', '')

    def _get_predicts_and_references(self, type_evaluation):
        references_anon  = []
        predictions_anon = []
        first_type = type_evaluation.split('_')[0]

        for d in self.data:
            for region in d['regions']:
                if not region['phrase']['amr']['amr_anon_pred']:
                    break
                
                predictions_anon.append(region['phrase'][first_type][type_evaluation + '_pred'] + '\n')
                references_anon.append( region['phrase'][first_type][type_evaluation + '_ref']  + '\n')
        
        return predictions_anon, references_anon

    def load_parsed(self, file_name):    
        data = dict()
        referencia = ''
        hipotese = ''
        key = ''
        for l in load_txt(file_name):
            #print(l)
            linha = l.replace('\n', '').replace('</s>', '').strip()
            #print(linha)
            #print(linha.isdigit())
            
            split = linha.split('-')
            if len(split) == 2 and split[0].isdigit() and split[1].isdigit():
                key  = linha
                #print('key = {}'.format(key))
                continue
            if linha in ['--------', '========'] :
                continue
                
            elif not referencia:
                referencia = linha
                
            else:
                hipotese = linha 
                data[key] = {'referencia': referencia, 'hipotese': hipotese}
                referencia = ''
                hipotese   = ''
                #break
            
        return data
    
    def create_file_to_convert_nl(self):
        ref  = []
        pred = []

        for d in self.data:
            id = str(d['id'])
            for i, region in enumerate(d['regions']):
                if region['phrase']['amr']['amr_anon_pred']:
                    pred.append({'id':'{}-{}'.format(id, i), 'amr':region['phrase']['amr']['amr_anon_pred'], 'sent': region['phrase']['ln']['ln_ref'] })
                    ref.append({'id':'{}-{}'.format(id, i), 'amr':region['phrase']['amr']['amr_anon_ref'], 'sent': region['phrase']['ln']['ln_ref'] })
            
        return ref, pred

    def build_ln(self, ln_pred, ln_ref):
        for d in self.data:
            for i, region in enumerate(d['regions']):
                key = '{}-{}'.format(d['id'], i)
                    
                if region['phrase']['amr']['amr_anon_pred']:                
                    region['phrase']['ln']['ln_pred'] = ln_pred[key]['hipotese']
                    region['phrase']['ln']['ln_ref_anon'] = ln_ref[key]['hipotese']    

    def parse(self, type_evaluation):
        predictions_anon, references_anon = self._get_predicts_and_references(type_evaluation)
        anon_full = simplifier.deAnonymizeAmr([references_anon, predictions_anon])
        self.load_anon_full(anon_full)

        if 'amr' in type_evaluation:
            
            ref, pred = self.create_file_to_convert_nl()

            save_json('neural-graph-to-seq-mp/ref.json', ref)
            save_json('neural-graph-to-seq-mp/pred.json', pred)

            path_current = os.getcwd()
            os.chdir(path_current + '/neural-graph-to-seq-mp')
            os.system('export CUDA_VISIBLE_DEVICES=0')
            os.system('python src_g2s/G2S_beam_decoder.py --model_prefix logs_g2s/G2S.silver_2m --in_path ref.json --out_path ref.parsed --mode beam')
            os.system('python src_g2s/G2S_beam_decoder.py --model_prefix logs_g2s/G2S.silver_2m --in_path pred.json --out_path pred.parsed --mode beam')
            os.chdir(path_current)
            
            ref_parsed  = self.load_parsed('neural-graph-to-seq-mp/ref.parsed')
            pred_parsed = self.load_parsed('neural-graph-to-seq-mp/pred.parsed')

            self.build_ln(pred_parsed, ref_parsed)