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
    embed.add_field(name='HP', value=f'{player.current_hp}/{player.max_hp}', inline=True)
    embed.add_field(name='MP', value=f'{player.current_mp}/{player.max_mp}', inline=True)
    embed.add_field(name='Strenght', value=f':crossed_swords: : {player.strenght}', inline=True)
    embed.add_field(name='Defense', value=f':shield: : {player.defense}', inline=True)
    embed.add_field(name='Magic', value=f':magic_wand: : {player.magic}', inline=True)
    embed.add_field(name='Speed', value=f':person_running:  : {player.speed}', inline=True)
    embed.add_field(name='Nex Lv', value=player.next_lv, inline=True)
    embed.add_field(name='Skill pts', value=player.skill_points, inline=False)

    return await ctx.send('', embed=embed)

@client.command(aliases=['sk'])
async def skills(ctx, arg='list'):
    """
    Lists skills learned or setted for this member.
    Accepted params: [list]|[set]
    default param: [list]
    """
    valid_args = ['set', 'list']
    user = ctx.message.author
    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    if arg not in valid_args:
        return await ctx.send(
            'Invalid argument. Accept only: **set** or **list**'
        )

    avatar_url = f'{ctx.message.author.avatar_url.BASE}/avatars/{user.id}/{user.avatar}'
    player = Player(**member, name=user.name)
    options = {
        'list': player.list_skills(),
        'set': player.get_skillset()
    }
    skills = options[arg]
    if not skills:
        return await ctx.send('User has no skills for this option!')

    skills = '\n'.join(str(skill) for skill in skills)

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=avatar_url)

    embed.add_field(name='Name', value=player.name, inline=False)
    embed.add_field(name='Skills', value=skills, inline=False)

    return await ctx.send('', embed=embed)
