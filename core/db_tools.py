from expiringdict import ExpiringDict
from pymongo import MongoClient
from orius.settings import MONGO_CONFIG
from core.util import next_lv, level_up
import logging
log = logging.getLogger()


# Active Time Battle: 10s wait time loader for player per server to use skills.
ATB = ExpiringDict(9999, 10)

class NotFoundOnDb(Exception):
    def __str__(self):
        return 'Object not found on database'


def set_base_stats(member):
    """
    Sets all base stats for a member.
    """
    member['lv'] = 1
    member['max_hp'] = 200
    member['max_mp'] = 100
    member['current_hp'] = 200
    member['current_mp'] = 100
    member['strength'] = 10
    member['defense'] = 10
    member['magic'] = 10
    member['next_lv'] = next_lv(member['lv'])

    return member


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
    member = next(cursor)

    if member.get('lv'):
        # If an Level attribute exists the the member has already been seted
        return member

    member = set_base_stats(member)
    member['skillset'] = []
    member['learned_skills'] = []
    member['items'] = []
    member['skill_points'] = 0
    member['kills'] = 0
    member['deaths'] = 0
    member['resets'] = []

    return member


def get_members(collection_name):
    """
    Get all registered members from a guild.
    param : collection_name : <str>
    return: <pymongo.cursor.Cursor>
    """
    collection = get_db()[collection_name]    
    return collection.find()


def update_member(collection_name, member_id, data):
    """
    Updates a member data on database.
    param : collection_name : <str>
    param : member_id : <str>
    param : data: <dict>
    return: <pymongo.cursor.Cursor>
    """
    collection = get_db()[collection_name]

    collection.create_index('member', unique=True)
    try:
        query = collection.update(
            {'member': member_id},
            data,
            upsert=True
        )
    except Exception as err:
        log.error(err)

    log.info('Identified member with id %s', member_id)

    # refreshs the query to get the member
    refresh = collection.find({'member': member_id})

    # verify if its a new member, adds base attributes if its new
    member = get_or_create_member(refresh)

    # calculates experience
    if member['lv'] < 100:
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
    return: <pymongo.cursor.Cursor>
    """
    collection = get_db()[collection_name]

    return collection.find({'member': member_id})


def get_members(collection_name):
    """
    Returns all members from a collection.
    """
    collection = get_db()[collection_name]

    return collection.find()


def reset_member(collection_name, member_id, member):
    """
    Resets a member to initial stats, keeping only the skill points earned
    before.
    param : collection_name : <str>
    param : member_id : <str>
    return : <pymongo.cursor.Cursor>
    """
    # this is a macgyvering for not having implemented member['resets'] as list before
    # ¯\_(ツ)_/¯
    resets = member['resets']
    if not resets:
        member['resets'] = [member['lv']]
    else:
        member['resets'].append(member['lv'])

    # calculates the amount skill points to start
    member['skill_points'] = sum([lv*2 for lv in member['resets']])

    # resets stats
    member = set_base_stats(member)

    # reset skills
    member['messages'] = 0
    member['skillset'] = []
    member['learned_skills'] = []

    # updates member in database
    collection = get_db()[collection_name]
    update = collection.update(
        {'member': member_id},
        member,
    )
    log.info(update)

    return member