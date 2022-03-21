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


def get_models():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "models.json")
    data = json.load(open(json_url))
    return data


def get_calling_codes():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "calling_codes.json")
    data = json.load(open(json_url))
    return data


def get_company():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "company.json")
    data = json.load(open(json_url))
    return data


def get_moduleCategories():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "module_categories.json")
    data = json.load(open(json_url))
    return data


def get_modules():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "modules.json")
    data = json.load(open(json_url))
    return data


def get_activities():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "activities.json")
    data = json.load(open(json_url))
    return data


def get_activity_types():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "activity_type.json")
    data = json.load(open(json_url))
    return data


def traverse_geoipdata(data):
    if 'ip' in data:
        ip_address = data['ip']
    else:
        ip_address = None
    if 'location' in data:
        if 'country' in data['location']:
            country = data['location']['country']
        else:
            country = None
        if 'region' in data['location']:
            region = data['location']['region']
        else:
            city = None
        if 'city' in data['location']:
            city = data['location']['city']
        else:
            city = None
        if 'lat' in data['location']:
            lat = data['location']['lat']
        else:
            lat = None
        if 'lng' in data['location']:
            lng = data['location']['lng']
        else:
            lng = None
        if 'postalcode' in data['location']:
            postalcode = data['location']['postalcode']
        else:
            postalcode = None
        if 'timezone' in data['location']:
            timezone = data['location']['timezone']
        else:
            timezone = None
        if 'geonameId' in data['location']:
            geonameId = data['location']['geonameId']
        else:
            geonameId = None
    else:
        country = None
        region = None
        city = None
        lat = None
        lng = None
        postalcode = None
        timezone = None
    if 'as' in data:
        if 'asn' in data['as']:
            asn = data['as']['asn']
        else:
            asn = None
        if 'name' in data['as']:
            name = data['as']['name']
        else:
            name = None
        if 'connectionType' in data['as']:
            connectionType = data['as']['connectionType']
        else:
            connectionType = None
    else:
        asn = None
        name = None
        connectionType = None

    return ip_address, country, region, city, lat, lng, postalcode, timezone, geonameId, asn, name, connectionType
