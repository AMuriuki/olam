from configparser import SafeConfigParser
import os
import json

parser = SafeConfigParser()


def updating(file, variables):
    parser.read(file)
    for k, v in variables.items():
        parser.set('tenant', k, v)
        with open(file, 'w') as configfile:
            parser.write(configfile)


def search_dict(values, searchFor):
    for k in values:
        for v in values[k]:
            if searchFor in v:
                return v
    return None


def get_countries():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "countries.json")
    data = json.load(open(json_url))
    return data


def get_countries_cities():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "world_cities.json")
    data = json.load(open(json_url))
    return data


def get_calling_codes():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "calling_codes.json")
    data = json.load(open(json_url))
    return data
