from config.connect import accidents as default_accident_collection
from typing import List, Optional, Dict
from pymongo.collection import Collection
from returns.maybe import Maybe

def find_all_accidents_by_area(area: str, collection: Collection = default_accident_collection) -> List[dict]:
    return list(collection.find({'area': area}))

# def find_car_by_id(id: str, collection: Collection = default_car_collection):
#     return Maybe.from_optional(collection.find_one({'_id': id}))
#
# def update_car_by_id(id: str, new_car: dict, collection: Collection = default_car_collection):
#     return collection.update_one({'_id': id}, {'$set': {
#         'license_id': new_car['license_id'],
#         'brand': new_car['brand'],
#         'color': new_car['color']
#         }})
#
# def delete_car_by_id(id: str, collection: Collection = default_car_collection):
#     return collection.delete_one({'_id': id})