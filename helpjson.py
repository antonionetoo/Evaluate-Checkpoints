import json

def load_json(file_name):
    data = None
    with open(file_name) as f:
        data = json.load(f)
    return data

def save_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f)   