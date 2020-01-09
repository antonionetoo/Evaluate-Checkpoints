# coding: utf-8

from helpjson import *
import sys
import io

def load_txt(name):
    with io.open(name, 'r',  encoding='utf8') as (f):
        return f.readlines()

data_amr         = load_json(sys.argv[1])

phrases_amr_anon = iter(load_txt(sys.argv[2]))

for d in data_amr:
    for r in d['regions']:
        r['phrase'] = next(phrases_amr_anon).replace('\n', '')
try:
    print(next(phrases_amr_anon))
    assert False
except StopIteration:
    print('ok!!!')

print(data_amr[0]['regions'][0]['phrase'])
name_json_output = sys.argv[1].split('.')[0] + '_anon.json'
print(name_json_output)
save_json(name_json_output, data_amr)
#python3 load_amr_anonimized.py vg/amr/region_descriptions_amr_anon.json vg/anon/phrases_amr.txt.anonymized 
