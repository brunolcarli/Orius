import logging
from random import random, randint
from core.character.skill import Skill
from core.db_tools import get_member, update_member, NotFoundOnDb
from core.util import get_damage, roll_d20


log = logging.getLogger()


class Player:
    """
    A player class is a represenation of a character, member or user.
    This class is cast over a mongo document, json or dict similiar structure
    to construct an object with a player behavior, so it can view status,
    skills and battle actions.

    The param : **attributes** is a duck typing implementation that, as
    mentioned before, expects a dict like object to init its self attributes.
    """
    def __init__(self, **attributes):
        self.lv = attributes.get('lv')
        self.name = attributes.get('name')
        self.max_hp = attributes.get('max_hp')
        self.max_mp = attributes.get('max_mp')
        self.current_hp = attributes.get('current_hp')
        self.current_mp = attributes.get('current_mp')
        self.strength = attributes.get('strength')
        self.defense = attributes.get('defense')
        self.magic = attributes.get('magic')
        self.next_lv = attributes.get('next_lv')
        self.messages = attributes.get('messages')
        self.skill_points = attributes.get('skill_points')
        self.learned_skills = attributes.get('learned_skills')
        self.skillset = attributes.get('skillset')
        self.items = attributes.get('items')
        self.resets = attributes.get('resets')
        self.kills = attributes.get('kills')
        self.deaths = attributes.get('deaths')

    def __repr__(self):
        """
        Returns a string representation fo the class.
        """
        return f'{self.name} Lv: {self.lv}'

    def is_alive(self):
        """
        Returns True if player is alive and False if its dead.
        """
        return True if self.current_hp > 0 else False

    def get_skills(self):
        """
        Returns a <dict> of <Skill> this player has learned keyed by skill name.
        """
        return {skill.get('name'): Skill(**skill) for skill in self.learned_skills}

    def get_skillset(self):
        """
        Returns a <dict> of <Skill> this player setted for combat.
        """
        return {skill.get('name'): Skill(**skill) for skill in self.skillset}

    def hit(self, damage):
        """
        Takes combat damage from attacking player.
        param : damage : <int>
        """
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0

    def attack(self, skill, target):
        """
        Atacks or use a skill on a target.
        param : skill : <Skill>
        param : target : <Player>
        return: <dict>
        """
        if skill.cost > self.current_mp:
            return {
                'hit': False,
                'target_alive': True,
                'log': 'Not enough move points!'
            }

        self.current_mp -= skill.cost

        # maps the damage base stats
        damage_base_stat = {
            'physical': self.strength,
            'magic': self.magic
        }
        defense_base_stat = {
            'physical': target.defense,
            'magic': target.magic
        }

        # calculates the total damage
        damage = get_damage(
            damage_base_stat[skill.type],
            skill.power,
            defense_base_stat[skill.type]
        )

        # the hands of destiny
        luck = roll_d20()

        # bad luck, attack missed
        if luck == 1:
            damage = 0
            luck_msg = f'\n{self.name} **missed** the hit.'

        # good luck, critical hit
        elif luck == 20:
            damage = int(damage * (randint(1, 2) + random()))
            luck_msg = '\nA **critical** hit, impressive!\n'\
                        f'{target.name} lost **{int(damage)}** hp.'

        # regular play
        else:
            luck_msg = f'\n{target.name} lost **{int(damage)}** hp.'

        target.hit(damage)

        log_msg = f'{self.name} used **{skill.name}** on {target.name}.' \
                  f'{luck_msg}'

        if not target.is_alive():
            self.kills += 1
            target.deaths += 1
            log_msg += f'\n{target.name} was **knocked out**.'

        log.info(log_msg)

        return {
            'hit': True,
            'target_alive': target.is_alive(),
            'log': log_msg
        }
