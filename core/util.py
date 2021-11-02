"""
General utilities and tools.
"""
from base64 import b64encode
from core.database import create_db_connection, read_query, DBQueries


def condition(column, value, operator='='):
    return {'column': column, 'operator': operator, 'value': value}


def make_atb_key(guild_id, member_id):
    """
    Makes a hash key to store member ATB on a timed expiring dict.
    The key is a base64 string withe the pattern guild_id:member_id.
    returns : <str>
    """
    return b64encode(f'{guild_id}:{member_id}'.encode('utf-8')).decode('utf-8')


def get_member_id(server_id, author_id):
    return f'{server_id}:{author_id}'


def get_member(member_id):
    """
    Returns a member data from database.
    param : member_id : <str>
    return: <list>
    """
    player = read_query(
        create_db_connection(),
        DBQueries.select_player(
            condition('member_id', member_id)
        )
    )
    return next(iter(player), None)


def get_members(guild):
    """
    Returns all members from a guild (discord server).
    """
    players = read_query(
        create_db_connection(),
        DBQueries.select_player(
            condition('guild', guild)
        )
    )
    return players
