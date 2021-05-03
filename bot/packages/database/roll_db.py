import pymongo
from ..files import config

client = pymongo.MongoClient(config.DB_STRING)
db = client[config.DB_NAME]
col_val = db[config.DB_COLLECTION_DAILY_ROLL_VALUE]
col_hist = db[config.DB_COLLECTION_DAILY_ROLL_HISTORY]
col_score = db[config.DB_COLLECTION_DAILY_ROLL_SCORE]


def get_roll_value(server_id):
    value = col_val.find_one(filter={'server_id': server_id})
    return value


def create_or_update_roll_value(server_id, value, date, user_id):
    if col_val.find_one(filter={'server_id': server_id}) is not None:
        update_value = {'$set': {'user_id': user_id,
                                 'date': date,
                                 'value': value}}
        col_val.update_one(filter={'server_id': server_id}, update=update_value)
    else:
        insert_value = {'user_id': user_id,
                        'server_id': server_id,
                        'date': date,
                        'value': value}
        col_val.insert_one(insert_value)


def get_roll_history(server_id, date):
    lst = col_hist.find(filter={'server_id': server_id,
                                'date': date})
    return lst


def add_roll_history(server_id, date, user_id, value):
    insert_value = {'server_id': server_id,
                    'user_id': user_id,
                    'date': date,
                    'value': value}
    col_hist.insert_one(insert_value)
