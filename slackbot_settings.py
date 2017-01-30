import os, json

settings_json = os.path.dirname(os.path.realpath(__file__)) + "/settings.json"

with open(settings_json) as data_file:
    data = json.load(data_file)

API_TOKEN = data['API_TOKEN']

DEFAULT_REPLY = "butt"




ERRORS_TO = data['ERRORS_TO']

PLUGINS = [
    'plugins.butte_plugin'
]

