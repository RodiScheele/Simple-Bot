import pymongo
from ..files import config

client = pymongo.MongoClient(config.DB_STRING)
db = client[config.DB_NAME]
col_val = db[config.DB_COLLECTION_DAILY_ROLL_VALUE]


def get_roll_value(server_name):
    value = col_val.find_one(filter={'server': server_name})
    return value


def create_or_update_roll_value(server_id, value, date, user_id):
    if col_val.find_one(filter={'server': server_id}) is not None:
        update_value = {'$set': {'user': user_id,
                                 'date': date,
                                 'value': value}}
        col_val.update_one(filter={'server': server_id}, update=update_value)
    else:
        insert_value = {'user': user_id,
                        'server': server_id,
                        'date': date,
                        'value': value}
        col_val.insert_one(insert_value)
