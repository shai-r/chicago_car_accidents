from config.connect import (accidents as default_accident_collection,
                            daily ,
                            weekly,
                            monthly )
from typing import List, Optional, Dict
from pymongo.collection import Collection
from returns.maybe import Maybe


def find_all_accidents_by_area(area, collection=default_accident_collection):
    cursor = collection.find({'area': f'{area}'})
    accidents_list = list(cursor)
    return accidents_list

def get_accidents_by_area_and_time(area, time_type, date):
    if time_type == 'd':
        return daily.find_one({'area': f'{area}', 'date': date})
    if time_type == 'w':
        return weekly.find({
            'area': f'{area}',
            'week_start': {'$lte': date},
            'week_end': {'$gte': date}
        })
    if time_type == 'm':
        date_split = date.split('-')
        return monthly.find_one({'year': date_split[0],'month': str(int(date_split[1])), 'area': f'{area}'})
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