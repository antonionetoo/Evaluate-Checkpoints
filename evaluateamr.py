import os, argparse, subprocess
from helptxt import save_txt
from helpjson import save_json
import csv

class EvaluateAMR:

    def __init__(self):
        self.results = dict()
        self.name_file_ref = 'amr_full_ref.txt'
        self.name_amr_anon_ref_full = 'amr_anon_ref_full.txt'
        self.name_anon_pred_full = 'amr_anon_pred_full.txt'

    def create_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-amr_full_ref')
        parser.add_argument('-amr_anon_ref_full')
        parser.add_argument('-amr_anon_pred_full')
        return parser.parse_args()

    def evaluate_smatch(self):
        self.results['smatch'] = list()
        os.chdir(self.path + '/smatch/')
        result = subprocess.Popen(('python3 smatch.py --significant 4 -f ../{} ../{}'.format(self.name_file_ref, self.name_amr_anon_ref_full)),
          shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['smatch'].append(result.decode().split('\n')[(-2)])
        result = subprocess.Popen(('python3 smatch.py --significant 4 -f ../{} ../{}'.format(self.name_file_ref, self.name_anon_pred_full)),
          shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['smatch'].append(result.decode().split('\n')[(-2)])
        result = subprocess.Popen(('python3 smatch.py --significant 4 -f ../{} ../{}'.format(self.name_amr_anon_ref_full, self.name_anon_pred_full)),
          shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['smatch'].append(result.decode().split('\n')[(-2)])

    def evaluate_sema(self):
        self.results['sema'] = []
        os.chdir(self.path + '/sema/')
        result = subprocess.Popen(('python3 sema.py -g ../{} -t ../{}'.format(self.name_file_ref, self.name_amr_anon_ref_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sema'].append(result.decode())
        result = subprocess.Popen(('python3 sema.py -g ../{} -t ../{}'.format(self.name_file_ref, self.name_anon_pred_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sema'].append(result.decode())
        result = subprocess.Popen(('python3 sema.py -g ../{} -t ../{}'.format(self.name_amr_anon_ref_full, self.name_anon_pred_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sema'].append(result.decode())

    def evaluate_sembleu(self):
        self.results['sembleu'] = []
        os.chdir(self.path + '/sembleu/')
        result = subprocess.Popen(('./eval.sh ../{1} ../{0}'.format(self.name_file_ref, self.name_amr_anon_ref_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sembleu'].append(result.decode().split('\n')[2])
        result = subprocess.Popen(('./eval.sh ../{1} ../{0}'.format(self.name_file_ref, self.name_anon_pred_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sembleu'].append(result.decode().split('\n')[2])
        result = subprocess.Popen(('./eval.sh ../{1} ../{0}'.format(self.name_amr_anon_ref_full, self.name_anon_pred_full)), shell=True,
          stdout=(subprocess.PIPE)).stdout.read()
        self.results['sembleu'].append(result.decode().split('\n')[2])

    def evaluate(self, ref_full, ref_anon_full, pred_anon_full):
        self.path = os.getcwd()
        save_txt(self.name_file_ref, ref_full)
        save_txt(self.name_amr_anon_ref_full, ref_anon_full)
        save_txt(self.name_anon_pred_full, pred_anon_full)
        self.evaluate_smatch()
        self.evaluate_sema()
        self.evaluate_sembleu()
        os.chdir(self.path)
        name_file_evaluate = 'evaluate_amr'
        save_json(name_file_evaluate + '.json', self.results)
