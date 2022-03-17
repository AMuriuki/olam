import os
import json


def get_accessGroups():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "access_groups.json")
    data = json.load(open(json_url))
    return data


def get_accessRights():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "data", "access_rights.json")
    data = json.load(open(json_url))
    return data


def get_accessGroupsRights():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(
        SITE_ROOT, "data", "access_rights_assosciations.json")
    data = json.load(open(json_url))
    return data
