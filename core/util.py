"""
General utilities and tools.
"""
from base64 import b64encode
from math import ceil
from random import randint, choice
from core.character.skill import SKILL_LIST
from orius.settings import GameConfig as config


def roll_d20():
    """
    Rolls a 20 sided dice.
    Returns a integer between 1 and 20.
    """
    return randint(1, 20)


def make_atb_key(guild_id, member_id):
    """
    Makes a hash key to store member ATB on a timed expiring dict.
    The key is a base64 string withe the pattern guild_id:member_id.
    returns : <str>
    """
    return b64encode(f'{guild_id}:{member_id}'.encode('utf-8')).decode('utf-8')


def get_member_skill_rank(lv):
    """
    Returns member skill rank based on his/her level.
    """
    if lv >= 1 and lv <= 10:
        return 'basic'

    elif lv >= 11 and lv <= 30:
        return 'champion'

    elif lv >= 31 and lv <= 50:
        return 'ultimate'

    else:
        return 'master'


def next_lv(level):
    """
    Calculates the amount Exp needed to level up based on the actual level.

    param : level : <int>
    """
    return ceil((2 * (level ** 2.6)) / 2)


def level_up(member):
    """
    Levels up a member, if possible.
    : param : member : <dict>
    return: <dict>
    """
    while member['messages'] >= member['next_lv'] and member.get('lv') < config.MAXIMUM_LV:
        member['lv'] += 1
        member['next_lv'] = next_lv(member['lv'])

        member['max_hp'] += randint(10, 50)
        member['max_mp'] += randint(5, 25)
        member['strength'] += randint(0, 2)
        member['defense'] += randint(0, 2)
        member['magic'] += randint(0, 2)
        member['skill_points'] += 2

        #pply  maximum restrictions
        if member['max_hp'] > config.MAXIMUM_HP:
            member['max_hp'] = config.MAXIMUM_HP

        if member['max_mp'] > config.MAXIMUM_MP:
            member['max_mp'] = config.MAXIMUM_MP

        if member['strength'] > config.MAXIMUM_STATS:
            member['strength'] = config.MAXIMUM_STATS

        if member['magic'] > config.MAXIMUM_STATS:
            member['magic'] = config.MAXIMUM_STATS

        if member['defense'] > config.MAXIMUM_STATS:
            member['defense'] = config.MAXIMUM_STATS

        # 50% chance learning a skill on level up
        if choice([True, False]):
            rank = get_member_skill_rank(member['lv'])
            new_skill = choice(SKILL_LIST[rank])

            # skip if member already knows this skill
            if new_skill not in member['learned_skills']:
                member['learned_skills'].append(new_skill)

    return member


def get_damage(player_power, skill_power, target_defense):
    """
    Calculates the battle damage.
    """
    damage = (player_power + skill_power - target_defense) / 2

    return damage if damage <= config.MAXIMUM_DAMAGE else MAXIMUM_DAMAGE
