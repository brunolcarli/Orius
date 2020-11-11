"""
Orius settings module.
"""
from decouple import config

__version__ = '0.0.1'

TOKEN = config('TOKEN', '')
SETTINGS_MODULE = config('SETTINGS_MODULE', 'common')
