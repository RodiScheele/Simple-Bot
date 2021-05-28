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


def get_roll_history_date(server_id, date):
    lst = col_hist.find(filter={'server_id': server_id,
                                'date': date})
    return lst


def get_roll_history_all(server_id):
    lst = col_hist.find(filter={'server_id': server_id})
    return lst


def get_roll_history_user(server_id, user_id):
    lst = col_hist.find(filter={'server_id': server_id,
                                'user_id': user_id})
    return lst


def add_roll_history(server_id, date, user_id, value):
    insert_value = {'server_id': server_id,
                    'user_id': user_id,
                    'date': date,
                    'value': value}
    col_hist.insert_one(insert_value)


def get_user_score(server_id, user_id):
    value = col_score.find_one(filter={'server_id': server_id,
                                       'user_id': user_id})
    return value


def get_server_score(server_id):
    value = col_score.find(filter={'server_id': server_id})
    return value


def create_or_update_score(server_id, user_id, score, user_name):
    if col_score.find_one(filter={'server_id': server_id, 'user_id': user_id}) is not None:
        update_value = {'$set': {'score': score,
                                 'user_name': user_name}}
        col_score.update_one(filter={'server_id': server_id, 'user_id': user_id}, update=update_value)
    else:
        insert_value = {'user_id': user_id,
                        'server_id': server_id,
                        'score': score,
                        'user_name': user_name}
        col_score.insert_one(insert_value)