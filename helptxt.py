def load_txt(name):
    with open(name, 'r') as f:
        return f.readlines()          

def save_txt(name, data):
    with open(name, 'w') as f:
        f.writelines(data)    