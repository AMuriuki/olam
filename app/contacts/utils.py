import os
import json


def get_partners():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "partners.json")
    data = json.load(open(json_url))
    return data
