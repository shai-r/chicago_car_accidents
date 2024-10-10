import csv
import os

from config.connect import chicago_car_accidents_db, daily, weekly, monthly


def read_csv(path: str):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def init_accidents():
    daily_docs = []
    weekly_docs = []
    monthly_docs = []
    data_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data.csv')
    for row in read_csv(data_path):
        c = 8

        crash_date = parse_date(row['CRASH_DATE'])
        area = row['BEAT_OF_OCCURRENCE']

        # Create daily document
        daily_doc = {
            'date': crash_date,
            'area': area,
            'total_accidents': 1,
            'injuries': {
                'total': safe_int(row['INJURIES_TOTAL']),
                'fatal': safe_int(row['INJURIES_FATAL']),
                'non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL'])
            },
            'contributing_factors': {
                row['PRIM_CONTRIBUTORY_CAUSE']: 1
            }
        }
        daily_docs.append(daily_doc)

        # Create weekly document
        week_start, week_end = get_week_range(crash_date)
        weekly_doc = {
            'week_start': str(week_start),
            'week_end': str(week_end),
            'area': area,
            'total_accidents': 1,
            'injuries': {
                'total': safe_int(row['INJURIES_TOTAL']),
                'fatal': safe_int(row['INJURIES_FATAL']),
                'non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL'])
            },
            'contributing_factors': {
                row['PRIM_CONTRIBUTORY_CAUSE']: 1
            }
        }
        weekly_docs.append(weekly_doc)

        # Create monthly document
        monthly_doc = {
            'year': str(crash_date.year),
            'month': str(crash_date.month),
            'area': area,
            'total_accidents': 1,
            'injuries': {
                'total': safe_int(row['INJURIES_TOTAL']),
                'fatal': safe_int(row['INJURIES_FATAL']),
                'non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL'])
            },
            'contributing_factors': {
                row['PRIM_CONTRIBUTORY_CAUSE']: 1
            }
        }
        monthly_docs.append(monthly_doc)
        if len(daily_docs) >= 1000:
            daily.insert_many(daily_docs)
            weekly.insert_many(weekly_docs)
            monthly.insert_many(monthly_docs)
            daily_docs = []
            weekly_docs = []
            monthly_docs = []


    if daily_docs:
        daily.insert_many(daily_docs)
        weekly.insert_many(weekly_docs)
        monthly.insert_many(monthly_docs)

init_accidents()