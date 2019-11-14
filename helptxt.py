import os.path

def load_txt(name):
    if os.path.exists(name):
        with open(name, 'r') as (f):
            return f.readlines()
    return []


def save_txt(name, data):
    with open(name, 'w') as (f):
        f.writelines(data)
