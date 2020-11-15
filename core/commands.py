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

    # Increments member message count
    update = update_member(
        collection_name=str(message.guild.id),
        member_id=str(message.author.id),
        data={'$inc': {'messages': 1}}
    )
    log.info(update)


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


@client.command(aliases=['ssk', 'assign', 'set'])
async def set_skill(ctx, skill_name=None):
    """
    Sets a skill to the skillset.
    A skill name must be specified.
        -> Example o:set_skill flame
    """
    if not skill_name:
        return await ctx.send('Must specify a skillname!')

    user = ctx.message.author
    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    # Player must have the skill before ssign it
    skills = member['learned_skills']
    skill_to_set = next(
        iter([skill for skill in skills if skill.get('name') == skill_name]),
        None
    )
    if not skill_to_set:
        return await ctx.send(f'Unknow skill {skill_name}')

    skillset = member['skillset']
    if len(skillset) >= 4:
        return await ctx.send('You can only hold up to 4 skills at once.')

    # Cant assign same skill twice
    if any([skill for skill in skillset if skill.get('name') == skill_name]):
        return await ctx.send('This skill is already assigned!')

    member['skillset'].append(skill_to_set)
    update = update_member(
        collection_name=str(ctx.message.guild.id),
        member_id=str(user.id),
        data=member
    )
    log.info(update_member)

    return await ctx.send(f'Assigned skill {skill_name} to the skillset!')


@client.command(aliases=['un', 'unassign', 'unset'])
async def unset_skill(ctx, skill_name=None):
    """
    Unassign a skill from the skillset.
    A skill name must be specified.
        -> Example o:unset_skill smash
    """
    if not skill_name:
        return await ctx.send('Must specify a skillname!')

    user = ctx.message.author
    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    # Player must have the skill before ssign it
    skillset = member['skillset']
    skill_to_unset = next(
        iter([skill for skill in skillset if skill.get('name') == skill_name]),
        None
    )
    if not skill_to_unset:
        return await ctx.send(f'Unknow skill {skill_name}')

    if len(skillset) <= 1:
        return await ctx.send('You cant hold less than 1 skill.')

    for skill in member['skillset']:
        if skill['name'] == skill_name:
            member['skillset'].remove(skill)

    update = update_member(
        collection_name=str(ctx.message.guild.id),
        member_id=str(user.id),
        data=member
    )
    log.info(update_member)

    return await ctx.send(f'Unassigned skill {skill_name} to the skillset!')

