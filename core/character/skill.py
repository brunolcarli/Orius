

class Skill:
    def __init__(self, **data):
        self.name = data.get('name')
        self.type = data.get('type')
        self.power = data.get('power')
        self.cost = data.get('cost')
        self.effect = data.get('effect')

    def __repr__(self):
        return f'{self.name} Move cost: {self.cost} Power: {self.power}'
