class PhraseConstructor:
    def __init__(self):
        pass

    def _construct_amr(self, amr_anon_ref, amr_full_ref):
        phrases = dict()

        phrases['amr_anon_ref']       = amr_anon_ref
        #referencia em amr anon e transformada em full
        phrases['amr_anon_ref_full']  = ''
        
        phrases['amr_anon_pred']      = ''
        #predita amr anon e transformada em full
        phrases['amr_anon_pred_full'] = ''

        phrases['amr_full_ref']       = amr_full_ref
        phrases['amr_full_pred']      = ''

        return phrases


    def _construct_nl(self, ln_ref):
        phrases             = dict()
        phrases['ln_ref']   = ln_ref
        phrases['ln_pred']  = ''
        
        #preditas a partir da anon de referencia
        phrases['ln_ref_anon']         = ''

        return phrases

    def construct_phrases(self, data, data_ln_anon_amr, type_evaluation):
        type = type_evaluation.split('_')[1]
        for j, d in enumerate(data):
            print(j)
            for r in d['regions']:                
                index = [i for i, v in enumerate(data_ln_anon_amr[type]) if v == r['phrase']]
                assert len(index) > 0
                i = index[0]        

                amr_anon_ref = data_ln_anon_amr['anon'][i].replace('  ', ' ')        
                amr_full_ref = data_ln_anon_amr['amr'][i]
                ln_ref = data_ln_anon_amr['ln'][i]

                r['phrase'] = dict()

                r['phrase']['amr'] = self._construct_amr(amr_anon_ref, amr_full_ref)
                r['phrase']['ln']  = self._construct_nl(ln_ref)            
   
                
        return data