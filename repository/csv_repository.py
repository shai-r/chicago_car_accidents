import csv
import os

from config.connect import daily, weekly, monthly, accidents
from utils.data_utils import parse_date, get_week_range, safe_int


def read_csv(path: str):
    with open(path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def find_in_docs(docs, key, value):
    for doc in docs:
        if doc[key] == value:
            return doc
    return None


def update_existing_doc(existing_doc, row):
    existing_doc['total_accidents'] += 1
    existing_doc['injuries']['total'] += safe_int(row['INJURIES_TOTAL'])
    existing_doc['injuries']['fatal'] += safe_int(row['INJURIES_FATAL'])
    existing_doc['injuries']['non_fatal'] += (safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL']))

    # Update contributing factors
    cause = row['PRIM_CONTRIBUTORY_CAUSE']
    if cause in existing_doc['contributing_factors']:
        existing_doc['contributing_factors'][cause] += 1
    else:
        existing_doc['contributing_factors'][cause] = 1


def init_accidents():
    daily_docs = []
    weekly_docs = []
    monthly_docs = []
    all_accidents = []
    data_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data.csv')

    for row in read_csv(data_path):
        crash_date = parse_date(row['CRASH_DATE'])
        area = row['BEAT_OF_OCCURRENCE']

        # Create a general document for all accidents
        accident_doc = {
            'date': str(crash_date.date()),
            'area': area,
            'injuries': {
                'total': safe_int(row['INJURIES_TOTAL']),
                'fatal': safe_int(row['INJURIES_FATAL']),
                'non_fatal': safe_int(row['INJURIES_TOTAL']) - safe_int(row['INJURIES_FATAL'])
            },
            'contributing_factors': {
                row['PRIM_CONTRIBUTORY_CAUSE']: 1
            }
        }


        all_accidents.append(accident_doc)
        accidents.insert_one(accident_doc)

        # Daily document
        daily_doc = {
            'date': str(crash_date.date()),
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

        # Check if the day already exists in MongoDB or local list
        existing_daily_doc = find_in_docs(daily_docs, 'date', crash_date) or daily.find_one({'date': crash_date, 'area': area})
        if existing_daily_doc:
            update_existing_doc(existing_daily_doc, row)
        else:
            daily_docs.append(daily_doc)

        # Weekly document
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

        # Check if the week already exists in MongoDB or local list
        existing_weekly_doc = find_in_docs(weekly_docs, 'week_start', str(week_start)) or weekly.find_one({'week_start': str(week_start), 'area': area})
        if existing_weekly_doc:
            update_existing_doc(existing_weekly_doc, row)
        else:
            weekly_docs.append(weekly_doc)

        # Monthly document
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

        # Check if the month already exists in MongoDB or local list
        existing_monthly_doc = find_in_docs(monthly_docs, 'month', str(crash_date.month)) or monthly.find_one({'year': str(crash_date.year), 'month': str(crash_date.month), 'area': area})
        if existing_monthly_doc:
            update_existing_doc(existing_monthly_doc, row)
        else:
            monthly_docs.append(monthly_doc)

        # Insert in batches to MongoDB
        if len(daily_docs) >= 1000:
            daily.insert_many(daily_docs)
            weekly.insert_many(weekly_docs)
            monthly.insert_many(monthly_docs)
            daily_docs = []
            weekly_docs = []
            monthly_docs = []

    # Insert any remaining documents at the end of the process
    if daily_docs:
        daily.insert_many(daily_docs)
    if weekly_docs:
        weekly.insert_many(weekly_docs)
    if monthly_docs:
        monthly.insert_many(monthly_docs)

