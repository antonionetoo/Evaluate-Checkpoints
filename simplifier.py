import subprocess
import os

def deAnonymizeAmr(anon):
    path_current = os.getcwd()

    amr_full = []
    for a in anon:
        amr = []
        for d in a:
            command = './anonDeAnon_java.sh deAnonymizeAmr false "%s"'%(d.replace('\n', ''))
            print(command)

            os.chdir(path_current + '/amr_simplifier')
            r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
            os.chdir(path_current)

            result = r.decode("utf-8")
            
            if 'FAILED_TO_PARSE' in result:
                amr.append(str(r) + '\n')
            else:
                amr.append(result.split('#')[0]+'\n\n')
                
        amr_full.append(amr)
    
    return amr_full