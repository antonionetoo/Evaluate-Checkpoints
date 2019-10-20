from phrasecorrector import PhraseCorrector

class LoadFromCheckpoint:
    def __init__(self):
        self.corrector = PhraseCorrector()

    def obtain_predict_and_reference(self, data):    
        references_and_predicts = []

        i = 0
        for linha in data:

            if not linha.startswith('IMG'):
                continue
            
            l = linha.replace('\n', '')

            i += 1
            predict       = l[l.find('PRED:')+6:l.find('GT:')-2]
            predict_fixed = self.corrector.fix_predict(predict)
            
            reference = l[l.find('GT:')+4:l.find(', OK')-2]
            id        = l[l.find('ID:')+4:l.find('PRED:')-1]
            
            references_and_predicts.append({'id':id, 'reference': reference, 'predict': predict_fixed})
        
        return references_and_predicts