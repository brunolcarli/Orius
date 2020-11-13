"""
General utilities and tools.
"""
from math import ceil
from random import randint, choice
from core.character.skill import SKILL_LIST


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

    if member['messages'] >= member['next_lv']:
        while member['messages'] >= member['next_lv']:
            member['lv'] += 1
            member['next_lv'] = next_lv(member['lv'])

            member['hp'] += randint(10, 50)
            member['mp'] += randint(5, 25)
            member['strenght'] += randint(0, 2)
            member['defense'] += randint(0, 2)
            member['magic'] += randint(0, 2)
            member['speed'] += randint(0, 1)
            member['skill_points'] += 2

            # 50% chance learning a skill on level up
            if choice([True, False]):
                rank = get_member_skill_rank(member['lv'])
                new_skill = choice(SKILL_LIST[rank])

                # skip if member already knows this skill
                if new_skill not in member['learned_skills']:
                    member['learned_skills'].append(new_skill)

    return member
