import subprocess, os

def deAnonymizeAmr(anon):
    path_current = os.getcwd()
    os.chdir(path_current + '/amr_simplifier')
    amr_full = []
    for a in anon:
        amr = []
        for d in a:
            command = './anonDeAnon_java.sh deAnonymizeAmr false "%s"' % d.replace('\n', '')

            r = subprocess.Popen(command, shell=True, stdout=(subprocess.PIPE)).stdout.read()
            result = r.decode('utf-8')
            if 'FAILED_TO_PARSE' in result:
                amr.append(str(result) + '\n')
            else:
                amr.append(result.split('#')[0] + '\n\n')

        amr_full.append(amr)

    os.chdir(path_current)
    return amr_full
