import logging
import json
import mysql.connector
from mysql.connector import Error
from orius.settings import MYSQL_CONFIG, SKILL_REGISTRATION_FILE


logger = logging.getLogger(__name__)

class DBQueries:
    """
    Implements raw SQL operation queries.
    """
    @staticmethod
    def create_schema(name):
        return f'CREATE SCHEMA {name}'

    @staticmethod
    def use_schema(name):
        return f'USE {name}'

    @staticmethod
    def create_player_table():
        query = '''
        CREATE TABLE Player (
            player_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            member_id VARCHAR(600) UNIQUE NOT NULL,
            lv INT DEFAULT 1,
            max_hp INT DEFAULT 200,
            max_mp INT DEFAULT 100,
            current_hp INT DEFAULT 200,
            current_mp INT DEFAULT 100,
            strength INT DEFAULT 10,
            defense INT DEFAULT 10,
            magic INT DEFAULT 10,
            skill_points INT DEFAULT 0,
            kills INT DEFAULT 0,
            deaths INT DEFAULT 0,
            resets TEXT,
            next_lv INT DEFAULT 1,
            skillset TEXT,
            learned_skills TEXT,
            exp INT DEFAULT 0,
            guild VARCHAR(255)
        )
        '''
        return query

    @staticmethod
    def create_skill_table():
        query = '''
        CREATE TABLE Skill (
            skill_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
            name VARCHAR(100) UNIQUE NOT NULL,
            type VARCHAR(8) NOT NULL,
            power INT NOT NULL,
            cost INT,
            effect TEXT,
            skill_rank VARCHAR(8)
        )
        '''
        return query

    @staticmethod
    def insert_player(member_id, guild_id):
        return f"INSERT INTO Player (member_id, guild) VALUES ('{member_id}', '{guild_id}')"

    @staticmethod
    def insert_skill(skill_data, skill_rank='basic'):
        name = skill_data.get('name')
        skill_type = skill_data.get('type')
        power = skill_data.get('power')
        cost = skill_data.get('cost')
        effect = skill_data.get('effect')
        query =  f"""
        INSERT INTO Skill
        (name, type, power, cost, effect, skill_rank)
        VALUES ('{name}', '{skill_type}', {power}, {cost}, '{effect}', '{skill_rank}')
        """
        return query

    @staticmethod
    def select_player(where=None):
        if not where:
            return 'SELECT * FROM Player'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM Player WHERE {condition}'

    @staticmethod
    def select_skill(where=None):
        if not where:
            return 'SELECT * FROM Skill'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        varchars = {'name', 'type', 'effect', 'skill_rank'}
        if column in varchars:
            condition = condition = f"{column} {operator} '{value}'"
        else:
            condition = f'{column} {operator} {value}'

        return f'SELECT * FROM Skill WHERE {condition}'

    @staticmethod
    def update_player(player_id, data):
        query = 'UPDATE Player SET '
        varchars = {'resets', 'learned_skills', 'skillset'}
        for field, value in data.items():
            if field in varchars:
                query += f" {field}='{value}',"
            else:
                query += f' {field}={value},'

        # remove the last comma (,)
        query = query[:-1]
        # Adds filter constraint
        query += f' WHERE player_id = {player_id}'

        return query


def db_connection(
    host_name=MYSQL_CONFIG['MYSQL_HOST'],
    user_name=MYSQL_CONFIG['MYSQL_USER'],
    user_password=MYSQL_CONFIG['MYSQL_PASSWORD']):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )
    except Error as err:
        logger.error('Error: %s', str(err))

    return connection


def create_db_connection(
    host_name=MYSQL_CONFIG['MYSQL_HOST'],
    user_name=MYSQL_CONFIG['MYSQL_USER'],
    user_password=MYSQL_CONFIG['MYSQL_PASSWORD'],
    db_name=MYSQL_CONFIG['MYSQL_DATABASE']):
    """
    Connects with database.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
    except Error as err:
        logger.error('Error: %s', str(err))

    return connection


def create_database(connection, query):
    """
    Create a new schema;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
    except Error as err:
        logger.error('Error: %s', str(err))


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as err:
        logger.error('Error: %s', str(err))


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        logger.error('Error: %s', str(err))


def init_db():
    """
    Initial migration script;
    Creates the schema and tables.
    *Run this function only in the first execution of the system*
    """
    try:
        with open(SKILL_REGISTRATION_FILE, 'r') as data:
            skills = json.load(data)
    except FileNotFoundError:
        raise Exception(f'Population file not found on {SKILL_REGISTRATION_FILE}!')

    if not skills:
        raise Exception('No skill found on population file!')

    con = db_connection()

    # Creates main schema and tables
    script = (
        DBQueries.create_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DBQueries.use_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DBQueries.create_player_table(),
        DBQueries.create_skill_table(),
    )
    for statement in script:
        execute_query(con, statement)
    logger.info('Database and tables created!')

    # populate with known skills
    for skill in skills:
        logging.info('Registering skill %s', skill["name"])
        query = DBQueries.insert_skill(skill, skill['rank'])
        execute_query(con, query)
    logging.info('Migration finished.')


def get_or_create_player(member_id, guild_id):
    condition = {'column': 'member_id', 'operator': '=', 'value': f"'{member_id}'"}
    query = DBQueries.select_player(where=condition)

    con = create_db_connection()
    result = read_query(con, query)

    if result:  # return the existent
        return next(iter(result))

    # object does not exist: create new
    query = DBQueries.insert_player(member_id, guild_id)
    execute_query(con, query)

    return get_or_create_player(member_id, guild_id)
