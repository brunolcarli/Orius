import logging
import sys
from orius.settings import TOKEN, __version__
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
        Discord RPG Bot
        '''
    )
    log.info('Running Orius version: %s\n', __version__)

    client.run(TOKEN)
