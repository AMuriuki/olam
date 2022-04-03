import os
import json


def get_purchase_status():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "purchase_status.json")
    data = json.load(open(json_url))
    return data


def get_purchases():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "purchases.json")
    data = json.load(open(json_url))
    return data
