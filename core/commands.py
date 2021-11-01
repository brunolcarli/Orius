import time
import logging
import discord
from discord.ext import commands, tasks
from orius.settings import __version__
from orius.settings import GameConfig as config
from core.util import make_atb_key, get_member_id
from core.db_tools import update_member, get_member, NotFoundOnDb, get_members, ATB, reset_member
from core.models import Player


client = commands.Bot(command_prefix='o:')
log = logging.getLogger()


class HealingWave(commands.Cog):
    """
    Loop for healing players time to time.
    """
    def __init__(self):
        self.guilds = client.guilds
        self.healing_loop.start()

    @tasks.loop(seconds=config.HEAL_TIME)
    async def healing_loop(self):
        """ Healing wave """
        log.info('healing servers...')
        for guild in self.guilds:
            log.info(guild.name)
            members = get_members(guild.id)

            for member in members:
                try:
                    member.current_hp += member.max_hp * config.HEAL_BUFF
                    if member.current_hp > member.max_hp:
                        member.current_hp = member.max_hp

                    member.current_mp += member.max_mp * config.HEAL_BUFF
                    if member.current_mp > member.max_mp:
                        member.current_mp = member.max_mp

                    member.save()
                except:
                    log.error('Failed to a heal member')


@client.event
async def on_ready():
    """
    Logs info message when initialized!
    """
    guilds = client.guilds
    client.add_cog(HealingWave())
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
    player = Player(
        message.author.name,
        get_member_id(message.guild.id, message.author.id)
    )
    player.exp_up(config.EXP_FACTOR)

    log.info('Updated member %s on %s', player.name, message.guild.id)


@client.command(aliases=['st'])
async def status(ctx):
    """
    Returns a member stats borad.
    """
    user = ctx.message.author
    guild = ctx.message.guild
    avatar_url = f'{ctx.message.author.avatar_url.BASE}/avatars/{user.id}/{user.avatar}'
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=avatar_url)

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    embed.add_field(name='Name', value=player.name, inline=False)
    embed.add_field(name='Lv', value=player.lv, inline=True)
    embed.add_field(name='HP', value=f'{int(player.current_hp)}/{player.max_hp}', inline=True)
    embed.add_field(name='MP', value=f'{int(player.current_mp)}/{player.max_mp}', inline=True)
    embed.add_field(name='strength', value=f':crossed_swords: : {player.strength}', inline=True)
    embed.add_field(name='Defense', value=f':shield: : {player.defense}', inline=True)
    embed.add_field(name='Magic', value=f':magic_wand: : {player.magic}', inline=True)
    embed.add_field(name='Nex Lv', value=f'{player.messages}/{player.next_lv}', inline=True)
    embed.add_field(name='Skill pts', value=player.skill_points, inline=True)
    embed.add_field(name='KOs', value=f':skull_crossbones:  {player.kills}', inline=True)
    embed.add_field(name='KOed', value=f':cross: {player.deaths}', inline=True)
    embed.add_field(name='Resets', value=f':arrows_counterclockwise: {player.get_resets()}', inline=True)

    return await ctx.send('', embed=embed)


@client.command(aliases=['sk', 'skill'])
async def skills(ctx, arg='list'):
    """
    Lists skills learned or setted for this member.
    Accepted params: [list]|[set]
    default param: [list]
    """
    valid_args = ['set', 'list']
    user = ctx.message.author
    guild = ctx.message.guild

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    if arg not in valid_args:
        return await ctx.send(
            'Invalid argument. Accept only: **set** or **list**'
        )

    avatar_url = f'{ctx.message.author.avatar_url.BASE}/avatars/{user.id}/{user.avatar}'
    options = {
        'list': player.get_skills(),
        'set': player.get_skillset()
    }
    skills = options[arg]
    if not skills:
        return await ctx.send('User has no skills for this option!')

    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.set_thumbnail(url=avatar_url)

    embed.add_field(name='Name', value=player.name, inline=False)
    for skill in list(skills.values()):
        embed.add_field(name=skill.name, value=skill, inline=True)

    return await ctx.send('', embed=embed)


@client.command(aliases=['ssk', 'assign', 'set'])
async def set_skill(ctx, *skill_name):
    """
    Sets a skill to the skillset.
    A skill name must be specified.
        -> Example o:set_skill flame
    """
    if not skill_name:
        return await ctx.send('Must specify a skillname!')

    skill_name = ' '.join(token for token in skill_name)
    user = ctx.message.author
    guild = ctx.message.guild

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    # Player must have the skill before assign it
    skills = player.get_skills()
    skill_to_set = next(
        iter([skill for skill in skills.values() if skill.name == skill_name]),
        None
    )
    if not skill_to_set:
        return await ctx.send(
            f'Unknow or unlearned skill {skill_name}.\n'\
            'List your skills with `o:skills`!'
        )

    skillset = player.get_skillset()
    if len(skillset) >= 4:
        return await ctx.send('You can only hold up to 4 skills at once.')

    # Cant assign same skill twice
    if any([skill for skill in skillset.values() if skill.name == skill_name]):
        return await ctx.send('This skill is already assigned!')

    player.set_skill(skill_to_set)
    log.info(update_member)

    return await ctx.send(f'Assigned skill {skill_name} to the skillset!')


@client.command(aliases=['un', 'unassign', 'unset'])
async def unset_skill(ctx, *skill_name):
    """
    Unassign a skill from the skillset.
    A skill name must be specified.
        -> Example o:unset_skill smash
    """
    if not skill_name:
        return await ctx.send('Must specify a skillname!')

    skill_name = ' '.join(token for token in skill_name)
    user = ctx.message.author
    guild = ctx.message.guild

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    # Player must have the skill before assign it
    skillset = player.get_skillset()
    skill_to_unset = next(
        iter([skill for skill in skillset.values() if skill.name == skill_name]),
        None
    )
    if not skill_to_unset:
        return await ctx.send(
            f'Unknow or unequipped skill {skill_name}.\n'\
            'List your equipped skills with `o:skills set`!'
        )

    if len(skillset) <= 1:
        return await ctx.send('You cant hold less than 1 skill.')

    for skill in skillset.values():
        if skill.name == skill_name:
            player.unset_skill(skill)
            return await ctx.send(f'Unassigned skill {skill_name} to the skillset!')


@client.command(aliases=['add', 'addst'])
async def add_stat(ctx, stat=None, value=''):
    """
    Increment an attribute stat spending your available skill points!
    An attribute and a value must be specified.
        -> Example: o:add_stat magic 1
    """
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

    user = ctx.message.author
    guild = ctx.message.guild

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    # member must have skill points AND the value specified
    skill_points = player.skill_points
    if not skill_points or value > skill_points:
        return await ctx.send('Not enough skill points.')

    # update member stats
    if stat == 'hp':
        stat = 'max_hp'
        if player.max_hp == config.MAXIMUM_HP:
            return await ctx.send('HP is already maximized!')

        player.skill_points -= value
        value = value *10
        player.max_hp += value
        if player.max_hp > config.MAXIMUM_HP:
            player.max_hp = config.MAXIMUM_HP

    elif stat == 'mp':
        stat = 'max_mp'
        if player.max_mp == config.MAXIMUM_MP:
            return await ctx.send('MP is already maximized!')

        player.skill_points -= value
        value = value * 10
        player.max_mp += value
        if player.max_mp > config.MAXIMUM_MP:
            player.max_mp = config.MAXIMUM_MP

    else:    
        if player.__getattribute__(stat) == config.MAXIMUM_STATS:
            return await ctx.send('This stat is already maximized!')

        player.__setattr__(stat, player.__getattribute__(stat) + value)
        player.skill_points -= value
        if player.__getattribute__(stat) > config.MAXIMUM_STATS:
            player.__setattr__(stat, config.MAXIMUM_STATS)
    player.save()

    return await ctx.send(
        f'Updated {stat} in {value}!\nSkill points left: {player.skill_points}'
    )


@client.command(aliases=['use', 'cast'])
async def use_skill(ctx, *skill_name):
    """
    Use a skill available on the skillset
    """
    mentions = ctx.message.mentions
    if not mentions:
        return await ctx.send('You must mention someone @Username')

    if not skill_name:
        return await ctx.send(
            'Must specify a skill and a target'\
            '\nExample: `o:use flame @foo`'
        )

    skill_name = ' '.join(token for token in skill_name).split('<')[0].strip()

    # get user from database
    user = ctx.message.author
    guild = ctx.message.guild

    try:
        attacker = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    # get target from database
    target = mentions[0]
    try:
        defender = Player(target.name, get_member_id(guild.id, target.id))
    except:
        return await ctx.send('Target member not found!')

    if user.id == target.id:
        return await ctx.send('You cant attack yourself!')

    # Check battle possibilities
    if not defender.is_alive():
        return await ctx.send('Cannot attack dead player!')

    if not attacker.is_alive():
        return await ctx.send('Dead player use no skills!')

    if skill_name not in attacker.get_skillset().keys():
        return await ctx.send(
            f'Unknow or unequipped skill {skill_name}.\n'\
            'List your skill set with `o:skills set`, '\
            'list all skills with `o:skills`, equip skills with `o:set skill_name`.'
        )

    member_atb = ATB.get(make_atb_key(guild.id, user.id))
    if member_atb:
        return await ctx.send('You have to wait 10s before next movement!') 

    # battle engage
    combat = attacker.attack(
        attacker.get_skillset()[skill_name],
        defender
    )
    attacker.save()
    defender.save()
    # next combat action have to wait 10 seconds
    ATB[make_atb_key(guild.id, user.id)] = True

    return await ctx.send(combat['log'])


@client.command(aliases=['rst'])
async def reset(ctx):
    """
    If a player level is above 50, he/she can resets the character.
    Reseting the character returns you to lv 1 with base stats and loose all
    your skills. But, in exchange you keep all skill points you earned before to
    spend again the way you want on your stats.
    """
    # get user from database
    user = ctx.message.author
    guild = ctx.message.guild

    try:
        player = Player(user.name, get_member_id(guild.id, user.id))
    except:
        return await ctx.send('Member not found!')

    if player.lv < 50:
        return await ctx.send(
            'You are not allowed to reset yet.\n' \
            'Only players with **lv 50** or higher are allowed to reset!'
        )
    player.reset()
    log.info('Reseting member %s', user.name)

    return await ctx.send('Reseted succesfull!')


@client.command(aliases=['sv', 'service', 'config', 'cfg'])
async def service_status(ctx):
    """
    Show Orius Service status and configurations.
    """
    heal_time = time.gmtime(config.HEAL_TIME)
    embed = discord.Embed(color=0x1E1E1E, type='rich')
    embed.add_field(
        name=':small_blue_diamond: Version',
        value=__version__,
        inline=True
    )
    embed.add_field(
        name=':fleur_de_lis: Discord Guilds count',
        value=len(ctx.bot.guilds),
        inline=False
    )
    embed.add_field(
        name=':scales: EXP Factor',
        value=f'x{config.EXP_FACTOR}',
        inline=True
    )
    embed.add_field(
        name=':adhesive_bandage: Healing time',
        value=f'{heal_time.tm_hour}:{heal_time.tm_min}:{heal_time.tm_sec}',
        inline=True
    )
    embed.add_field(
        name=':sparkles: Healing Factor',
        value=f'{int(config.HEAL_BUFF * 100)}%',
        inline=True
    )
    embed.add_field(
        name=':shinto_shrine: This Guild',
        value=ctx.guild.name,
        inline=True
    )
    embed.add_field(
        name=':family_mwg: Guild members registered',
        value=len(get_members(ctx.guild.id)),
        inline=True
    )
    embed.add_field(
        name=':notebook: Docs',
        value='`https://github.com/brunolcarli/Orius/wiki`',
        inline=True
    )

    return await ctx.send(':gear: Showing service info! :gear:', embed=embed)    


@client.command(aliases=['sm'])
async def summon(ctx, *enemy_name):
    pass


@client.command()
async def foo(ctx):
    member_id = get_member_id(ctx.guild.id, ctx.author.id)
    player = Player('baz', member_id)
    player.get_skills()
    return await ctx.send('foo')
