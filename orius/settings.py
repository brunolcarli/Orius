"""
Orius settings module.
"""
import os

__version__ = '0.0.1'

TOKEN = os.environ.get('TOKEN', '')

MONGO_CONFIG = {
    'MONGO_HOST': os.environ.get('MONGO_HOST', 'mongodb://localhost'),
    'MONGO_PORT': os.environ.get('MONGO_PORT', '27017'),
    'MONGO_DATABASE': os.environ.get('MONGO_DATABASE'),
    'MONGO_USER': os.environ.get('MONGO_USER'),
    'MONGO_PASS': os.environ.get('MONGO_PASS')
}

