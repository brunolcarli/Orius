"""
General utilities and tools.
"""
from math import ceil
from random import randint


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

    return member
