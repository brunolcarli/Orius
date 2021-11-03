from random import randint
from math import ceil
from expiringdict import ExpiringDict
from orius.settings import GameConfig as config


# Active Time Battle: 10s wait time loader for player per server to use skills.
ATB = ExpiringDict(9999, 10)


def roll_d20():
    """
    Rolls a 20 sided dice.
    Returns a integer between 1 and 20.
    """
    return randint(1, 20)


def next_lv(level):
    """
    Calculates the amount Exp needed to level up based on the actual level.

    param : level : <int>
    """
    return ceil((2 * (level ** 2.6)) / 2)


def get_damage(player_power, skill_power, target_defense, lv):
    """
    Calculates the battle damage.
    """
    damage = ((player_power + skill_power - target_defense) / 2) + (lv * 2)

    # min damage is 1
    if damage <= 0:
        damage = 1

    return damage if damage <= config.MAXIMUM_DAMAGE else config.MAXIMUM_DAMAGE


def set_base_stats(player):
    """
    Sets all base stats for a member.
    """
    player.lv = 1
    player.max_hp = 200
    player.max_mp = 100
    player.current_hp = 200
    player.current_mp = 100
    player.strength = 10
    player.defense = 10
    player.magic = 10
    player.next_lv = next_lv(player.lv)
    player.messages = 0
    player.learned_skills = '[]'
    player.skillset = '[]'
    player.save()

    return player