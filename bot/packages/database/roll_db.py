import pymongo
from ..files import config

client = pymongo.MongoClient(config.DB_STRING)
db = client[config.DB_NAME]
col_val = db[config.DB_COLLECTION_DAILY_ROLL_VALUE]


def get_roll_value(server_id):
    value = col_val.find_one(filter={'server_id': server_id})
    return value


def create_or_update_roll_value(server_id, value, datetime, user_id):
    if col_val.find_one(filter={'server_id': server_id}) is not None:
        update_value = {'$set': {'user_id': user_id,
                                 'date': datetime,
                                 'value': value}}
        col_val.update_one(filter={'server': server_id}, update=update_value)
    else:
        insert_value = {'user_id': user_id,
                        'server_id': server_id,
                        'datetime': datetime,
                        'value': value}
        col_val.insert_one(insert_value)
