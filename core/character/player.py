

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
        self.skills = attributes.get('skills')

    def __str__(self):
        return f'{self.name} Lv: {self.lv}'

    def is_alive(self):
        return True if self.hp > 0 else False

    def get_damage(self, damage):
        self.hp -= damage

        if self.hp <= 0:
            self.hp = 0

        return self.is_alive()

    def hit(self, skill):  # TODO <- fazer uma classe skill, montar a logica de dano
        pass

    def attack(self, skill, target):
        return target.hit(skill)
