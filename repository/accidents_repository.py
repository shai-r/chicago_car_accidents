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


def get_injury_stats_by_area2(area):
    pipeline = [
        {'$match': {'area': area}},
        {'$unwind': '$accidents'},
        {'$group': {
            '_id': '$area',
            'totalInjuries': {'$sum': '$accidents.injuries.total'},
            'totalFatal': {'$sum': '$accidents.injuries.fatal'},
            'totalNonFatal': {'$sum': '$accidents.injuries.non_fatal'},
            'fatalAccidents': {
                '$push': {
                    '$cond': [
                        {'$gt': ['$accidents.injuries.fatal', 0]},
                        {
                            'date': '$accidents.date',
                            'cause': '$accidents.PRIM_CONTRIBUTORY_CAUSE',
                            'fatalCount': '$accidents.injuries.fatal'
                        },
                        None
                    ]
                }
            },
            'nonFatalAccidents': {
                '$push': {
                    '$cond': [
                        {
                            '$and': [
                                {'$eq': ['$accidents.injuries.fatal', 0]},
                                {'$gt': ['$accidents.injuries.non_fatal', 0]}
                            ]
                        },
                        {
                            'date': '$accidents.date',
                            'cause': '$accidents.PRIM_CONTRIBUTORY_CAUSE',
                            'nonFatalCount': '$accidents.injuries.non_fatal'
                        },
                        None
                    ]
                }
            }
        }},
        {'$project': {
            '_id': 0,
            'area': '$_id',
            'totalInjuries': 1,
            'totalFatal': 1,
            'totalNonFatal': 1,
            'fatalAccidents': {
                '$filter': {
                    'input': '$fatalAccidents',
                    'as': 'accident',
                    'cond': {'$ne': ['$$accident', None]}
                }
            },
            'nonFatalAccidents': {
                '$filter': {
                    'input': '$nonFatalAccidents',
                    'as': 'accident',
                    'cond': {'$ne': ['$$accident', None]}
                }
            }
        }}
    ]
    return list(default_accident_collection.aggregate(pipeline))

