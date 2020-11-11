import logging
import discord
from discord.ext import commands, tasks
from orius.settings import __version__

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
