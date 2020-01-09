from helpjson import *
from copy import deepcopy
import sys

data     = load_json(sys.argv[1])
data_amr = load_json(sys.argv[2])

errors                = 0
total_regions         = 0
total_regions_correct = 0
without_regions       = 0
new_data              = []

for i, d in enumerate(data):
    new_instance = dict()
    new_instance['id']      = d['id']
    new_instance['regions'] = []

    if len(d['regions']) == 0:
        without_regions += 1
        continue

    for j, r in enumerate(d['regions']):
        total_regions += 1
        try:
            phrase      = data_amr[r['phrase'].strip().replace('\n', '')].replace('  ', '')
        except KeyError:
            errors += 1
            print('{}-{}:{}'.format(i, j, r['phrase']))
            continue

        total_regions_correct += 1
        new_region             = deepcopy(r)
        new_region['phrase']   = phrase
        new_instance['regions'].append(new_region)
        
    if len(new_instance['regions']) > 0:
        new_data.append(new_instance)


assert without_regions + len(new_data) == len(data)
assert total_regions == errors + total_regions_correct

name = sys.argv[1].split('.')
print(name[0] + '_amr.' + name[1])

save_json(name[0] + '_amr.' + name[1], new_data)
#python3 phrase_to_amr.py vg/ln/region_descriptions.json senteces_amr.json