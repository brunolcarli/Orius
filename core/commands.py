import logging
import discord
from discord.ext import commands, tasks
from orius.settings import __version__

from core.db_tools import update_member

client = commands.Bot(command_prefix='o:')
log = logging.getLogger()


@client.event
async def on_ready():
    """
    Logs info message when initialized!
    """
    log.info('Orius ready and standing by!')


@client.command(aliases=['v'])
async def version(ctx):
    """
    Shows Orius version
    """
    await ctx.send(__version__)


@client.event
async def on_message(message):
    """
    Chat message handler.
    """
    channel = message.channel

    # Do not process other bot messages
    if message.author.bot:
        return

    # Give priority for bot prefixed commands
    await client.process_commands(message)

    x = update_member(str(message.guild.id), str(message.author.id))
    print(x)