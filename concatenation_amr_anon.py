
from helpjson import *
from copy import deepcopy

#phrases = load_txt(sys.argv[2])

delimiter = '&'

def concatenation(data):
    for d in data:
        for r in d['regions']:
            
            phrase_non_spaced = ' '.join(r['phrase'].split())

            tokens = phrase_non_spaced.split()

            for i, t in enumerate(tokens):
                if t.startswith(':') and not i == len(tokens) - 1:
                        
                    if tokens[i+1] == '(':
                        continue
                    
                    tokens[i] = tokens[i+1] + delimiter  + t 
                    tokens.pop(i+1)

            r['phrase'] = ' '.join(tokens)

def deconcatenation_phrase(phrase):
    tokens = phrase.split()

    for i, t in enumerate(tokens):
        if delimiter in t:
            split = t.split(delimiter)

            tokens.pop(i)
            tokens.insert(i, split[1])
            tokens.insert(i+1, split[0])

    return  ' '.join(tokens)    

def deconcatenation(data):
    for d in data:
        for r in d['regions']:
            r['phrase'] = deconcatenation_phrase(r['phrase'])
            


if __name__ == '__main__':
    from copy import deepcopy

    data = load_json('google_refexp_amr_anon.json')

    concatenation(data)
    data_concatenation = deepcopy(data)
    deconcatenation(data)

    data2 = load_json('google_refexp_amr_anon.json')

    for i, d in enumerate(data):
        for j, r in enumerate(d['regions']):
            phrase_non_spaced = ' '.join(data2[i]['regions'][j]['phrase'].split())
            assert r['phrase'] == phrase_non_spaced
    
    save_json('google_refexp_amr_anon_concatenation.json', data_concatenation)


ids_to_removed = []
for i, d in enumerate(data):
    for j, r in enumerate(d['regions']):
        phrase = ' '.join(data2[i]['regions'][j]['phrase'].split())
        if not deconcatenation_phrase(r['phrase']) == phrase:
            ids_to_removed.append((i, j))
            print('{}-{}'.format(i, j))
            #print(deconcatenation_phrase(r['phrase']))
            #print(data2[i]['regions'][j]['phrase'])

for i in ids_to_removed:
    del data