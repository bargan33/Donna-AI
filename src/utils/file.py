import re
import os
import json



def parse_json_file(path_to_json_file:     str) -> dict:
    f = open(path_to_json_file)
    return json.load(f)

def save_to_json_file(data: dict, path_to_json_file: str):
    with open(path_to_json_file, 'w') as outfile:
        json.dump(data, outfile)