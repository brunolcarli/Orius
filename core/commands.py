import logging
import discord
from discord.ext import commands, tasks
from orius.settings import __version__

from core.db_tools import update_member, get_member, NotFoundOnDb, get_members
from core.character.player import Player

client = commands.Bot(command_prefix='o:')
log = logging.getLogger()


class GuildTracker(commands.Cog):
    """
    Loop for healing players time to time.
    """
    def __init__(self):
        self.guilds = client.guilds
        self.healing_loop.start()

    @tasks.loop(seconds=3600)
    async def healing_loop(self):
        """ Tracking task """
        log.info('tracking...')
        for guild in self.guilds:
            log.info(guild.name)
            members = get_members(str(guild.id))

            for member in members:
                member['current_hp'] += member['max_hp'] * .1
                if member['current_hp'] > member['max_hp']:
                    member['current_hp'] = member['max_hp']

                member['current_mp'] += member['max_mp'] * .1
                if member['current_mp'] > member['max_mp']:
                    member['current_mp'] = member['max_mp']

                update_member(str(guild.id), str(member['member']), data=member)


@client.event
async def on_ready():
    """
    Logs info message when initialized!
    """
    guilds = client.guilds
    client.add_cog(GuildTracker())
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
    embed.add_field(name='Name', value=player.name, inline=False)
    embed.add_field(name='Lv', value=player.lv, inline=True)
    embed.add_field(name='HP', value=f'{int(player.current_hp)}/{player.max_hp}', inline=True)
    embed.add_field(name='MP', value=f'{int(player.current_mp)}/{player.max_mp}', inline=True)
    embed.add_field(name='strength', value=f':crossed_swords: : {player.strength}', inline=True)
    embed.add_field(name='Defense', value=f':shield: : {player.defense}', inline=True)
    embed.add_field(name='Magic', value=f':magic_wand: : {player.magic}', inline=True)
    embed.add_field(name='Nex Lv', value=player.next_lv, inline=True)
    embed.add_field(name='Skill pts', value=player.skill_points, inline=True)
    embed.add_field(name='KOs', value=f':skull_crossbones:  {player.kills}', inline=True)
    embed.add_field(name='KOed', value=f':cross: {player.deaths}', inline=True)
    embed.add_field(name='Resets', value=f':arrows_counterclockwise: {player.resets}', inline=True)

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


@client.command(aliases=['add', 'addst'])
async def add_stat(ctx, stat=None, value=''):
    """
    Increment an attribut stat spending your available skill points!
    An attribute and a value must be specified.
        -> Example: o:add_stat magic 1
    """
    print('++++++++++')
    print(value)
    print('++++++++++')
    if not stat and not value:
        return await ctx.send(
            'Must specify attribute and value:\n`o:add magic 1`'
        )

    # value must be a integer number
    if not value.isdigit():
        return await ctx.send('The skill point value must be a integer number!')
    value = int(value)

    # stat must be valid
    valid_stats = set(['strength', 'magic', 'defense', 'hp', 'mp',])
    if stat not in valid_stats:
        return await ctx.send(
            f'Invalid stat attribute {stat} \
            \nValid stats are {" ".join(f"`{s}`" for s in list(valid_stats))}'
        )

    # get member from database
    user = ctx.message.author
    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    # member must have skill points AND the value specified
    skill_points = member.get('skill_points')
    if not skill_points or value > skill_points:
        return await ctx.send('Not enough skill points.')

    # update member stats
    if stat == 'hp':
        stat = 'max_hp'
        member['skill_points'] -= value
        value = value *10
        member[stat] += value

    elif stat == 'mp':
        stat = 'max_mp'
        member['skill_points'] -= value
        value = value * 10
        member[stat] += value

    else:
        member[stat] += value
        member['skill_points'] -= value

    update = update_member(
        collection_name=str(ctx.message.guild.id),
        member_id=str(user.id),
        data=member
    )
    log.info(update_member)

    return await ctx.send(
        f'Updated {stat} in {value}!\nSkill points left: {member["skill_points"]}'
    )


@client.command(aliases=['use', 'cast'])
async def use_skill(ctx, skill_name=None):
    """
    Use a skill available on the skillset
    """
    if not skill_name:
        return await ctx.send(
            'Must specify a skill and a target'\
            '\nExample: `o:use flame @foo`'
        )

    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    # get user from database
    user = ctx.message.author
    member = next(get_member(str(ctx.message.guild.id), str(user.id)))
    if not member:
        return await ctx.send('Member not found!')

    # get target from databse
    target = mentions[0]
    target_member = next(get_member(str(ctx.message.guild.id), str(target.id)))
    if not target_member:
        return await ctx.send('Target not found on database.')

    attacker = Player(**member, name=user.name)
    defender = Player(**target_member, name=target.name)

    # Check battle possibilities
    if not defender.is_alive():
        return await ctx.send('Cant attack dead player!')

    if not attacker.is_alive():
        return await ctx.send('Dead player use no skills!')

    if skill_name not in attacker.get_skillset().keys():
        return await ctx.send(f'Unknow skill {skill_name}')

    # battle engage
    combat = attacker.attack(
        attacker.get_skillset()[skill_name],
        defender
    )

    # updates defender data on database
    target_member['current_hp'] = defender.current_hp
    target_member['deaths'] = defender.deaths
    update_defender = update_member(
        collection_name=str(ctx.message.guild.id),
        member_id=str(user.id),
        data=target_member
    )
    log.info(update_defender)

    # updates attacker data on database
    member['current_mp'] = attacker.current_mp
    member['kills'] = attacker.kills
    update_attacker = update_member(
        collection_name=str(ctx.message.guild.id),
        member_id=str(user.id),
        data=member
    )
    log.info(update_attacker)

    return await ctx.send(combat['log'])
