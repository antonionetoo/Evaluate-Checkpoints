import subprocess
from helptxt import *
import os


def deAnonymizeAmr(files_name):
    path_current = os.getcwd()
    for file_name in files_name:
        data = load_txt(file_name)

        data_amr_full = []
        for _, d in enumerate(data):
            command = './anonDeAnon_java.sh deAnonymizeAmr false "%s"'%(d.replace('\n', ''))
            print(command)

            os.chdir(path_current + '/amr_simplifier')
            r = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()
            os.chdir(path_current)

            result = r.decode("utf-8")
            
            if 'FAILED_TO_PARSE' in result:
                data_amr_full.append(str(r) + '\n')
            else:
                data_amr_full.append(result.split('#')[0]+'\n\n')

        name_new_file = '_full.'.join(file_name.split('.'))
        
        print(name_new_file)
        print(type(name_new_file))
        save_txt(str(name_new_file), data_amr_full)

        #break

