from typing import Dict

import json
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))

def convert_accidents_by_area_to_json(accident):
    return {
        'id': parse_json(accident['_id']),
        'area': accident['area'],
        'injuries': convert_injuries_to_json(accident['injuries']),
        'contributing_factors': accident['contributing_factors']
    }

def convert_injuries_to_json(injuries) -> Dict[str, str]:
    return {
        'total': injuries['total'],
        'fatal': injuries['fatal'],
        'non_fatal': injuries['non_fatal'],
    }