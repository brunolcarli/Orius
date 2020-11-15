from pymongo import MongoClient
from orius.settings import MONGO_CONFIG
from core.util import next_lv, level_up
import logging
log = logging.getLogger()


def get_db():
    """
    Returns a mongo client connection cursor for database defined on
    settings.
    """
    user = MONGO_CONFIG['MONGO_USER']
    pwd = MONGO_CONFIG['MONGO_PASS']
    host = MONGO_CONFIG['MONGO_HOST']
    port = MONGO_CONFIG['MONGO_PORT']

    client = MongoClient(f'mongodb://{user}:{pwd}@{host}:{port}')

    return client[MONGO_CONFIG['MONGO_DATABASE']]


def get_or_create_member(cursor):
    """
    Check if the member is a new member, adding default attributes or return
    the member if it already exists.

    param : cursor : <pymongo.cursor.Cursor>
    """
    member = cursor.next()

    if member.get('lv'):
        # If an Level attribute exists the the member has already been seted
        return member

    # Define default attributes
    member['lv'] = 1
    member['max_hp'] = 200
    member['max_mp'] = 100
    member['current_hp'] = 200
    member['current_mp'] = 100
    member['strenght'] = 10
    member['defense'] = 10
    member['magic'] = 10
    member['speed'] = 8
    member['skillset'] = []
    member['learned_skills'] = []
    member['skill_points'] = 0
    member['kills'] = 0
    member['deaths'] = 0
    member['resets'] = 0
    member['next_lv'] = next_lv(member['lv'])

    return member


def update_member(collection_name, member_id, data):
    """
    Updates a member data on database.
    param : collection_name : <str>
    param : member_id : <str>
    param : data: <dict>
    return: <pymongo.cursor.Cursor>
    """
    collection = get_db()[collection_name]

    query = collection.update(
        {'member': member_id},
        data,
        upsert=True
    )
    log.info('Created memeber with id %s', member_id)

    # refreshs the query to get the member
    refresh = collection.find({'member': member_id})

    # verify if its a new member, adds base attributes if its new
    member = get_or_create_member(refresh)

    # calculates experience
    level_up(member)

    query = collection.update(
        {'member': member_id},
        member,
    )
    log.info('Updated member %s', member_id)

    return member


def get_member(collection_name, member_id):
    """
    Returns a member data from database.
    param : collection_name : <str>
    param : member_id : <str>
    retur: <pymongo.cursor.Cursor>
    """
    collection = get_db()[collection_name]

    return collection.find({'member': member_id})
