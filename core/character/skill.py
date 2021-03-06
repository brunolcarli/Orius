

class Skill:
    def __init__(self, **data):
        self.name = data.get('name')
        self.type = data.get('type')
        self.power = data.get('power')
        self.cost = data.get('cost')
        self.effect = data.get('effect')

    def __repr__(self):
        emojis = {
            'physical': ':crossed_swords:',
            'magic': ':magic_wand:'
        }
        return f'{emojis[self.type]} | MP: {self.cost} | Power: {self.power}'


# hardcoded available skills
SKILL_LIST = {
    'basic': [
        {'name': 'punch', 'type': 'physical', 'power': 10, 'cost': 1, 'effect': None},
        {'name': 'kick', 'type': 'physical', 'power': 20, 'cost': 2, 'effect': None},
        {'name': 'throw', 'type': 'physical', 'power': 22, 'cost': 2, 'effect': None},
        {'name': 'slash', 'type': 'physical', 'power': 30, 'cost': 3, 'effect': None},
        {'name': 'smash', 'type': 'physical', 'power': 30, 'cost': 3, 'effect': None},
        {'name': 'headbutt', 'type': 'physical', 'power': 30, 'cost': 3, 'effect': None},
        {'name': 'flame', 'type': 'magic', 'power': 20, 'cost': 3, 'effect': None},
        {'name': 'shock', 'type': 'magic', 'power': 20, 'cost': 3, 'effect': None},
        {'name': 'snowball', 'type': 'magic', 'power': 20, 'cost': 3, 'effect': None},
        {'name': 'windcutter', 'type': 'magic', 'power': 30, 'cost': 4, 'effect': None},
        {'name': 'hail', 'type': 'magic', 'power': 30, 'cost': 4, 'effect': None},
        {'name': 'light sword', 'type': 'magic', 'power': 35, 'cost': 5, 'effect': None},
        {'name': 'dark saber', 'type': 'magic', 'power': 50, 'cost': 2, 'effect': None},
        # {'name': 'war cry', 'type': 'buff', 'power': 0, 'cost': 5, 'effect': 'strength +10%'},
        # {'name': 'meditation', 'type': 'buff', 'power': 0, 'cost': 5, 'effect': 'magic +10%'},
        # {'name': 'work up', 'type': 'buff', 'power': 0, 'cost': 5, 'effect': 'defense +10%'},
    ],
    'champion': [
        {'name': 'super punch', 'type': 'physical', 'power': 40, 'cost': 5, 'effect': None},
        {'name': 'high kick', 'type': 'physical', 'power': 45, 'cost': 6, 'effect': None},
        {'name': 'suplex', 'type': 'physical', 'power': 50, 'cost': 7, 'effect': None},
        {'name': 'hammer hand', 'type': 'physical', 'power': 50, 'cost': 7, 'effect': None},
        {'name': 'rib breaker', 'type': 'physical', 'power': 55, 'cost': 7, 'effect': None},
        {'name': 'fireball', 'type': 'magic', 'power': 45, 'cost': 7, 'effect': None},
        {'name': 'gust', 'type': 'magic', 'power': 45, 'cost': 7, 'effect': None},
        {'name': 'flush', 'type': 'magic', 'power': 50, 'cost': 8, 'effect': None},
        {'name': 'pressure', 'type': 'magic', 'power': 55, 'cost': 8, 'effect': None},
        {'name': 'high voltage', 'type': 'magic', 'power': 60, 'cost': 8, 'effect': None},
        {'name': 'freeze', 'type': 'magic', 'power': 62, 'cost': 8, 'effect': None},
        {'name': 'uppercut', 'type': 'physical', 'power': 42, 'cost': 8, 'effect': None},
        {'name': 'armlock', 'type': 'physical', 'power': 40, 'cost': 8, 'effect': None},
        {'name': 'toxic vapor', 'type': 'magic', 'power': 55, 'cost': 8, 'effect': None},
        {'name': 'scalp', 'type': 'physical', 'power': 45, 'cost': 8, 'effect': None},
        {'name': 'burn', 'type': 'magic', 'power': 60, 'cost': 8, 'effect': None},
        {'name': 'liquid jet', 'type': 'magic', 'power': 45, 'cost': 8, 'effect': None},
        {'name': 'light arrow', 'type': 'magic', 'power': 65, 'cost': 10, 'effect': None},
        {'name': 'dark sworn', 'type': 'magic', 'power': 78, 'cost': 35, 'effect': None},
        # {'name': 'agility', 'type': 'buff', 'power': 0, 'cost': 10, 'effect': 'speed +5%'},
        # {'name': 'cure', 'type': 'buff', 'power': 0, 'cost': 10, 'effect': 'recover 15% hp'},
    ],
    'ultimate': [
        {'name': 'stone breaker', 'type': 'physical', 'power': 75, 'cost': 15, 'effect': None},
        {'name': 'ground shake', 'type': 'physical', 'power': 75, 'cost': 15, 'effect': None},
        {'name': 'hyper smash', 'type': 'physical', 'power': 75, 'cost': 15, 'effect': None},
        {'name': 'thrust', 'type': 'physical', 'power': 75, 'cost': 15, 'effect': None},
        {'name': 'sandstorm', 'type': 'magic', 'power': 70, 'cost': 15, 'effect': None},
        {'name': 'hailstorm', 'type': 'magic', 'power': 70, 'cost': 15, 'effect': None},
        {'name': 'tornado', 'type': 'magic', 'power': 75, 'cost': 17, 'effect': None},
        {'name': 'firestorm', 'type': 'magic', 'power': 80, 'cost': 20, 'effect': None},
        {'name': 'light spear', 'type': 'magic', 'power': 86, 'cost': 18, 'effect': None},
        {'name': 'dark wave', 'type': 'magic', 'power': 70, 'cost': 8, 'effect': None},
        # {'name': 'rest', 'type': 'buff', 'power': 0, 'cost': 1, 'effect': 'recover 10% hp'},
    ],
    'master': [
        {'name': 'overpush', 'type': 'physical', 'power': 90, 'cost': 20, 'effect': None},
        {'name': 'backstab', 'type': 'physical', 'power': 90, 'cost': 20, 'effect': None},
        {'name': 'head smash', 'type': 'physical', 'power': 90, 'cost': 20, 'effect': None},
        {'name': 'super nova', 'type': 'magic', 'power': 90, 'cost': 22, 'effect': None},
        {'name': 'star pulse', 'type': 'magic', 'power': 90, 'cost': 20, 'effect': None},
        {'name': 'meteor', 'type': 'magic', 'power': 100, 'cost': 25, 'effect': None},
        {'name': 'light storm', 'type': 'magic', 'power': 120, 'cost': 30, 'effect': None},
        {'name': 'dark end', 'type': 'magic', 'power': 150, 'cost': 70, 'effect': None},
        {'name': 'murder', 'type': 'physical', 'power': 100, 'cost': 35, 'effect': None},
        # {'name': 'barrier', 'type': 'buff', 'power': 0, 'cost': 15, 'effect': 'defense +25%'},
        # {'name': 'concentrate', 'type': 'buff', 'power': 0, 'cost': 15, 'effect': 'magic +25%'},
        # {'name': 'dragon spirit', 'type': 'buff', 'power': 0, 'cost': 15, 'effect': 'strength +25%'},
    ],
}
