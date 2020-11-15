from core.character.skill import Skill


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
        self.strenght = attributes.get('strenght')
        self.defense = attributes.get('defense')
        self.magic = attributes.get('magic')
        self.speed = attributes.get('speed')
        self.next_lv = attributes.get('next_lv')
        self.messages = attributes.get('messages')
        self.skill_points = attributes.get('skill_points')
        self.learned_skills = attributes.get('learned_skills')
        self.skillset = attributes.get('skillset')
        self.items = attributes.get('items')
        self.resets = attributes.get('resets')
        self.kills = attributes.get('kills')
        self.deaths = attributes.get('deaths')
        self.delay = attributes.get('delay')

    def __repr__(self):
        """
        Returns a string representation fo the class.
        """
        return f'{self.name} Lv: {self.lv}'

    def is_alive(self):
        """
        Returns True if player is alive and False if its dead.
        """
        return True if self.hp > 0 else False

    def list_skills(self):
        """
        Returns a <list> of <Skill> this player has learned.
        """
        return [Skill(**skill) for skill in self.learned_skills]

    def get_skillset(self):
        """
        Returns a <list> of <Skill> this player setted for combat.
        """
        return [Skill(**skill) for skill in self.skillset]

    def get_skill(self, skill_name):
        """
        Returns a <Skill> based on its name.
        param: skill_name : <str>
        """
        skill = [skill for skill in self.skills if skill.get('name') == skill_name]
        return next(Skill(**skill))

    def get_damage(self, damage):
        """
        Decreases player health points (hp) equal to damage taken.
        Returns True if player still alive after the damage and False if dies.
        param : damage : <int>
        """
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0

        return self.is_alive()

    def hit(self, skill):  # TODO <- fazer uma classe skill, montar a logica de dano
        pass

    def attack(self, skill, target):
        """
        Atacks or use a skill on a target.
        param : skill : <Skill>
        param : target : <Player>
        return: <dict>
        """
        if skill.cost > self.mp:
            return {
                'hit': False,
                'target_alive': True,
                'log': 'Not enough move points!'
            }

        self.mp -= skill.cost

        return {
            'hit': True,
            'target_alive': target.hit(skill),
            'log': f'Hit target with {skill}'
        }

