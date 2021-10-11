import os
import json


def get_recurring_plans():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "recurring_plans.json")
    data = json.load(open(json_url))
    return data


def get_stages():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "stages.json")
    data = json.load(open(json_url))
    return data
