
class BuilderPredictions:

    def __init__(self):
        self.types_by_input = {'anon': ['amr', 'amr_anon_ref', 'amr_anon_pred'], 
                               'ln': ['ln', 'ln_ref', 'ln_pred']}

    def construct_index_by_id(self, data):
        self.index_by_id = dict()
        for i, d in enumerate(data):
            id = d['id']
            if id in self.index_by_id:
                assert False, 'error construct_index_by_id'
            else:
                self.index_by_id[id] = i

    def build_predictions(self, references_predtions, data, type_evaluation):
        keys = self.types_by_input[type_evaluation]

        self.construct_index_by_id(data)
        for d in references_predtions:
            index = self.index_by_id[int(d['id'])]
            reference = d['reference']
            for region in data[index]['regions']:
                if (' ').join(region['phrase'][keys[0]][keys[1]].split()) == reference:
                    region['phrase'][keys[0]][keys[2]] = d['predict']
                    data[index]['test'] = True
                    break
            else:
                amr_anon_ref = [ region['phrase'][keys[0]][keys[1]] for region in data[index]['regions'] ]
                if ('. ').join(amr_anon_ref) == reference:
                    data[index]['test'] = True
                    for region in data[index]['regions']:
                        region['phrase'][keys[0]][keys[1]] = reference
                        region['phrase'][keys[0]][keys[2]] = d['predict']

                else:
                    print (d['id'])
                    print (reference)
                    assert False, 'build_predictions'

        return data
