# coding: utf-8

import sys
from helpjson import *
import codecs

def save_txt(name, data):
    with codecs.open(name, 'w', 'utf-8') as (f):
        for d in data:
            f.write(d)

data = load_json(sys.argv[1])
phrases_amr = []
errors = 0

for i, d in enumerate(data):
    regions_deleted = []
    for j, r in enumerate(d['regions']):
        phrase = r['phrase'].replace('  ', '').replace('\n', '')
        if '~' in phrase:
            regions_deleted.append(j)
            continue

        phrases_amr.append(phrase + '\n')        

    errors += len(regions_deleted)    
    for delet in regions_deleted:
        print('i:{} j:{} len = {}'.format(i, j, len(d['regions'])))
        del d['regions'][delet]

print('{} erros'.format(errors))
save_txt('phrases_amr.txt', phrases_amr)

name_json_output = sys.argv[1].split('.')[0] + '_anon.json'
print(name_json_output)
save_json(name_json_output, data)
