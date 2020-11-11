import logging
import sys
from orius.settings import TOKEN, SETTINGS_MODULE, __version__
from core.commands import client

logging.basicConfig(level='INFO')
log = logging.getLogger()

if __name__ == '__main__':
    log.info(
        '''
        ============
        ┌─┐┬─┐┬┬ ┬┌─┐
        │ │├┬┘││ │└─┐
        └─┘┴└─┴└─┘└─┘
        =============
        Dicord RPG Bot
        '''
    )
    log.info('Running Orius version: %s\n', __version__)

    client.run(TOKEN)
