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

def get_accidents_by_cause(area):
    pipeline = [
        {'$match': {'area': area}},
        {'$group': {
            '_id': '$contributing_factors',
            'count': {'$sum': 1}
        }}
    ]
    return list(default_accident_collection.aggregate(pipeline))


def get_injury_stats_by_area(area):
    pipeline = [
        {'$match': {'area': area}},
        {'$group': {
            '_id': None,
            'total_injuries': {'$sum': '$injuries.total'},
            'fatal_injuries': {'$sum': '$injuries.fatal'},
            'non_fatal_injuries': {'$sum': '$injuries.non_fatal'},
            'events': {'$push': {
                'date': '$date',
                'injuries': '$injuries'
            }}
        }}
    ]
    return list(default_accident_collection.aggregate(pipeline))
# def group_by_main_cause(area):
#     res = default_accident_collection.aggregate([
#         {'$match': {'area': area}},
#         {'$group': {'_id': '$main_cause', 'count': {'$sum': 1},'total injury': {'$sum': '$injuries.total' }, 'fatal': {'$sum': '$injuries.fatal' } }},
#         {'$sort': {'fatal': -1}}
#     ])
#     return list(res)
#
# def statistics_by_region(area):
#     res = default_accident_collection.aggregate([
#         {'$match': {'area': area}},
#         {'$project': {'_id': 0}},
#         {'$group': {'_id': '$region',
#                     'total injury': {'$sum': '$injuries.total' },
#                     'fatal': {'$sum': '$injuries.fatal' },
#                     'non_fatal': {'$sum': '$injuries.non_fatal' },
#                     'all accidents': {'$push':'$$ROOT'}}}
#     ])
#     return list(res)