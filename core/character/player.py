from core.character.skill import Skill


class Player:
    def __init__(self, **attributes):
        self.lv = attributes.get('lv')
        self.name = attributes.get('name')
        self.hp = attributes.get('hp')
        self.mp = attributes.get('mp')
        self.strenght = attributes.get('strenght')
        self.defense = attributes.get('defense')
        self.magic = attributes.get('magic')
        self.speed = attributes.get('speed')
        self.next_lv = attributes.get('next_lv')
        self.messages = attributes.get('messages')
        self.skill_points = attributes.get('skill_points')
        self.learned_skills = attributes.get('learned_skills')
        self.skillset = attributes.get('skillset')

    def __repr__(self):
        return f'{self.name} Lv: {self.lv}'

    def is_alive(self):
        return True if self.hp > 0 else False

    def list_skills(self):
        return [Skill(**skill) for skill in self.learned_skills]

    def get_skillset(self):
        return [Skill(**skill) for skill in self.skillset]

    def get_skill(self, skill_name):
        skill = [skill for skill in self.skills if skill.get('name') == skill_name]
        return next(Skill(**skill))

    def learn_skill(self, skill):
        if len(self.skills) >= 4:
            return {'learned': False, 'log': 'Cant learn any more skills.'}

        # TODO adicionar skill no banco de dados
        self.skills.append(skill)
        return {'learned': True, 'log': f'learned {Skill(**skill)}'}

    def get_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0

        return self.is_alive()

    def hit(self, skill):  # TODO <- fazer uma classe skill, montar a logica de dano
        pass

    def attack(self, skill, target):
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

