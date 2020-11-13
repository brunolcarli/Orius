import logging
import discord
from discord.ext import commands, tasks
from orius.settings import __version__

from core.db_tools import update_member, get_member
from core.character.player import Player

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


@client.command(aliases=['st'])
async def status(ctx):
    """
    Returns a member stats borad.
    """
    user = ctx.message.author
    avatar_url = f'{ctx.message.author.avatar_url.BASE}/avatars/{user.id}/{user.avatar}'
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=avatar_url)

    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    player = Player(**member, name=user.name)
    embed.add_field(name='Name', value=player.name, inline=True)
    embed.add_field(name='Lv', value=player.lv, inline=True)
    embed.add_field(name='HP', value=player.hp, inline=True)
    embed.add_field(name='MP', value=player.mp, inline=True)
    embed.add_field(name='Strenght', value=f':crossed_swords: : {player.strenght}', inline=True)
    embed.add_field(name='Defense', value=f':shield: : {player.defense}', inline=True)
    embed.add_field(name='Magic', value=f':magic_wand: : {player.magic}', inline=True)
    embed.add_field(name='Speed', value=f':person_running:  : {player.speed}', inline=True)
    embed.add_field(name='Nex Lv', value=player.next_lv, inline=True)

    return await ctx.send('', embed=embed)
