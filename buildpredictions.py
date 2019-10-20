class BuilderPredictions():

    def __init__(self):
        pass
    
    def construct_index_by_id(self, data):
        self.index_by_id = dict()
        for i, d in enumerate(data):
            id = d['id']
            if id in self.index_by_id:
                assert False, 'error construct_index_by_id'
            else:
                self.index_by_id[id] = i
        

    def build_predictions(self, references_predtions, data, type_evaluation):
        type = type_evaluation.split('_')[0]
        
        self.construct_index_by_id(data)

        for d in references_predtions:
            index = self.index_by_id[int(d['id'])]
            reference = d['reference']

            for region in data[index]['regions']:
                if region['phrase'][type][type + '_anon_ref'] == reference: 
                    region['phrase'][type][type + '_anon_pred'] = d['predict']
                    break
            else:
                #fusion regins
                amr_anon_ref = [region['phrase'][type][type + '_anon_ref'] for region in data[index]['regions']]
                if '. '.join(amr_anon_ref) == reference:
                    for region in data[index]['regions']:
                        region['phrase'][type][type + '_anon_pred'] = d['predict']
                else:
                    assert False, 'build_predictions'
                        
        return data   
