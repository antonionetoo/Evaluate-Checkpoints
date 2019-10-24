import subprocess
import os
from helptxt import load_txt

def deAnonymizeAmr(anon):
    path_current = os.getcwd()

    amr_full = []
    os.chdir(path_current + '/amr_simplifier')
    for a in anon:
        amr = []
        for d in a:
            command = './anonDeAnon_java.sh deAnonymizeAmr false "%s" > out.txt'%(d.replace('\n', ''))
            print(command)
            os.system(command)
            result = load_txt('out.txt')[0]
            
            if 'FAILED_TO_PARSE' in result:
                amr.append(str(result) + '\n')
            else:
                amr.append(result.split('#')[0]+'\n\n')
                
        amr_full.append(amr)
        
    os.chdir(path_current)
    return amr_full