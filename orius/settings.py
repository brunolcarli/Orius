"""
Orius settings module.
"""
import os

__version__ = '1.4.4'

TOKEN = os.environ.get('TOKEN', '')

MONGO_CONFIG = {
    'MONGO_HOST': os.environ.get('MONGO_HOST', 'mongodb://localhost'),
    'MONGO_PORT': os.environ.get('MONGO_PORT', '27017'),
    'MONGO_DATABASE': os.environ.get('MONGO_DATABASE'),
    'MONGO_USER': os.environ.get('MONGO_USER'),
    'MONGO_PASS': os.environ.get('MONGO_PASS')
}

MYSQL_CONFIG = {
    'MYSQL_HOST': os.environ.get('MYSQL_HOST', 'localhost'),
    'MYSQL_USER': os.environ.get('MYSQL_USER', 'guest'),
    'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE', 'orius'),
    'MYSQL_ROOT_PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD', '')
}


class GameConfig:
    """
    General game settings.
    """
    # stats stuff
    MAXIMUM_HP = 9999
    MAXIMUM_MP = 999
    MAXIMUM_STATS = 999
    MAXIMUM_RESETS = 999
    MAXIMUM_LV = 100
    MAXIMUM_DAMAGE = 9999

    # internal mechanics
    EXP_FACTOR = int(os.environ.get('EXP_FACTOR', 1))
    HEAL_TIME = int(os.environ.get('HEAL_TIME', 3600))
    HEAL_BUFF = float(os.environ.get('HEAL_BUFF', .1))
