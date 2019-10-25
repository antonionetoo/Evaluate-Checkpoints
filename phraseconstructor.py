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
    
    def _indexes_by_phrase(self, data, data_ln_anon_amr, type):
        indexes_ln = dict()
        for i, d in enumerate(data_ln_anon_amr['ln']):
            
            assert not d in indexes_ln
            indexes_ln[d] = i

        self.indexes = dict()

        for i, d in enumerate(data):
            for j, region in enumerate(d['regions']):
                phrase = region['phrase']
                index = indexes_ln[phrase]

                key = '{}-{}'.format(d['id'], j)
                self.indexes[key] = index

    def construct_phrases(self, data, data_ln, data_ln_anon_amr, type_evaluation):
        type = type_evaluation.split('_')[1]
        self._indexes_by_phrase(data_ln, data_ln_anon_amr, type)

        for d in data:
            for i, r in enumerate(d['regions']):
                key = '{}-{}'.format(d['id'], i)
                index = self.indexes[key]


                amr_anon_ref = data_ln_anon_amr['anon'][index].replace('  ', ' ')        
                amr_full_ref = data_ln_anon_amr['amr'][index]
                ln_ref       = data_ln_anon_amr['ln'][index]

                r['phrase'] = dict()

                r['phrase']['amr'] = self._construct_amr(amr_anon_ref, amr_full_ref)
                r['phrase']['ln']  = self._construct_nl(ln_ref)            
                   
        return data