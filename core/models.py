import json
from ast import literal_eval as convert
from random import randint, random, choice
from orius.settings import GameConfig as config
from core.database import (create_db_connection, execute_query,
                           get_or_create_player, read_query, DBQueries)
from core.util import get_damage, roll_d20, condition, set_base_stats, next_lv


class Player:
    """
    A player class is a represenation of a character, member or user.
    This class is cast over a mysql row structure to construct an object with a
    player behavior, so it can view status, skills and battle actions.
    """
    def __init__(self, name, member_id, data=None):
        if not data:
            # resolve from db
            user = get_or_create_player(member_id, member_id.split(':')[0])
        else:
            # resolve from param
            user = data

        resets = '[]' if not user[13] else user[13]
        skillset = '[]' if not user[15] else user[15]
        learned_skills = '[]' if not user[16] else user[16]

        # set attributes
        self.name = name
        self.id = user[0]
        self.lv = user[2]
        self.max_hp = user[3]
        self.max_mp = user[4]
        self.current_hp = user[5]
        self.current_mp = user[6]
        self.strength = user[7]
        self.defense = user[8]
        self.magic = user[9]
        self.skill_points = user[10]
        self.kills = user[11]
        self.deaths = user[12]
        self.resets = resets
        self.next_lv = user[14]
        self.skillset = skillset
        self.learned_skills = learned_skills
        self.messages = user[17]  # messages is the EXP acquired

    def __repr__(self):
        """
        Returns a string representation fo the class.
        """
        return f'{self.name} Lv: {self.lv}'

    def save(self):
        """
        Save current attributes to permanet file on database.
        """
        con = create_db_connection()
        execute_query(
            con,
            DBQueries.update_player(self.id, self.get_attributes_data())
        )

    def is_alive(self):
        """
        Returns True if player is alive and False if its dead.
        """
        return True if self.current_hp > 0 else False

    def get_skills(self):
        """
        Returns a <dict> of <Skill> this player has learned keyed by skill name.
        """
        skills =  [Skill(i) for i in convert(self.learned_skills)]
        return {skill.name: skill for skill in skills}

    def get_skillset(self):
        """
        Returns a <dict> of <Skill> this player setted for combat.
        """
        skills =  [Skill(i) for i in convert(self.skillset)]
        return {skill.name: skill for skill in skills}

    def get_resets(self):
        return len(convert(self.resets))

    def hit(self, damage):
        """
        Takes combat damage from attacking player.
        param : damage : <int>
        """
        self.current_hp -= damage

        if self.current_hp <= 0:
            self.current_hp = 0
        self.save()

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
            defense_base_stat[skill.type],
            self.lv
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

        self.save()
        print(log_msg)

        return {
            'hit': True,
            'target_alive': target.is_alive(),
            'log': log_msg,
            'attacker': self,
            'defender': target
        }

    def get_attributes_data(self):
        data = {
            'lv': self.lv,
            'max_hp': self.max_hp,
            'max_mp': self.max_mp,
            'current_hp': self.current_hp,
            'current_mp': self.current_mp,
            'strength': self.strength,
            'defense': self.defense,
            'magic': self.magic,
            'skill_points': self.skill_points,
            'kills': self.kills,
            'deaths': self.deaths,
            'resets': self.resets,
            'next_lv': self.next_lv,
            'skillset': self.skillset,
            'learned_skills': self.learned_skills,
            'exp': self.messages
        }
        return data

    def get_skill_rank(self):
        """
        Returns member skill rank based on his/her level.
        """
        if self.lv >= 1 and self.lv <= 10:
            return 'basic'

        elif self.lv >= 11 and self.lv <= 30:
            return 'champion'

        elif self.lv >= 31 and self.lv <= 50:
            return 'ultimate'

        else:
            return 'master'

    def exp_up(self, factor=1):
        self.messages += factor

        if self.messages >= self.next_lv:
            self.lv_up()

        self.save()

    def lv_up(self):
        """
        Levels up a member, if possible.
        """
        while self.messages >= self.next_lv and self.lv < config.MAXIMUM_LV:
            self.lv += 1
            self.next_lv = next_lv(self.lv)

            self.max_hp += randint(10, 50)
            self.max_mp += randint(5, 25)
            self.strength += randint(0, 2)
            self.defense += randint(0, 2)
            self.magic += randint(0, 2)
            self.skill_points += 2

            #pply  maximum restrictions
            if self.max_hp > config.MAXIMUM_HP:
                self.max_hp = config.MAXIMUM_HP

            if self.max_mp > config.MAXIMUM_MP:
                self.max_mp = config.MAXIMUM_MP

            if self.strength > config.MAXIMUM_STATS:
                self.strength = config.MAXIMUM_STATS

            if self.magic > config.MAXIMUM_STATS:
                self.magic = config.MAXIMUM_STATS

            if self.defense > config.MAXIMUM_STATS:
                self.defense = config.MAXIMUM_STATS

            # 50% chance learning a skill on level up

            if choice([True, False]):
                skills_data = read_query(
                    create_db_connection(),
                    DBQueries.select_skill(
                        condition('skill_rank', self.get_skill_rank())
                    )
                )
                new_skill = choice([s[0] for s in skills_data])
                skills = convert(self.learned_skills)

                # skip if member already knows this skill
                if new_skill not in skills:
                    skills.append(new_skill)
                    self.learned_skills = str(skills)

        self.save()
        return self

    def set_skill(self, skill):
        skills = convert(self.learned_skills)
        skillset = convert(self.skillset)

        skillset.append(skill.skill_id)
        self.skillset = str(skillset)
        self.save()

    def unset_skill(self, skill):
        skills = convert(self.learned_skills)
        skillset = convert(self.skillset)

        skillset.pop(skillset.index(skill.skill_id))
        self.skillset = str(skillset)
        self.save()

    def reset(self):
        """
        Resets a player to initial stats, keeping only the skill points earned
        before.
        """
        # resets is a list of the last lv(s) player has reseted
        resets = convert(self.resets)
        resets.append(self.lv)

        # calculates the amount skill points to start
        total_sp = sum([lv*2 for lv in resets])
        self.skill_points = total_sp
        self.resets = str(resets)

        # resets stats and skills
        player = set_base_stats(self)

        return player


class Skill:
    def __init__(self, reference, resolver='skill_id'):
        # resolve from db
        skill = next(
            iter(read_query(
                create_db_connection(),
                DBQueries.select_skill(condition(resolver, reference))
            )),
            None
        )
        # TODO raise exception if not skill
        self.skill_id = skill[0]
        self.name = skill[1]
        self.type = skill[2]
        self.power = skill[3]
        self.cost = skill[4]
        self.effect = skill[5]
        self.rank = skill[6]

    def __repr__(self):
        emojis = {
            'physical': ':crossed_swords:',
            'magic': ':magic_wand:'
        }
        return f'{emojis[self.type]} | MP: {self.cost} | Power: {self.power}'
