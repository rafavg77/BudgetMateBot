import json

def load_config():
    # Lee los valores del archivo de configuración.
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config