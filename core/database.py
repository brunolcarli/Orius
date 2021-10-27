import mysql.connector
from mysql.connector import Error
from orius.settings import MYSQL_CONFIG


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
            resets INT DEFAULT 0,
            next_lv INT DEFAULT 1,
            skillset TEXT,
            learned_skills TEXT,
            exp INT DEFAULT 0
        )
        '''
        return query

    @staticmethod
    def insert_player(member_id):
        return f"INSERT INTO Player (member_id) VALUES ('{member_id}')"

    @staticmethod
    def select_player(where=None):
        if not where:
            return 'SELECT * FROM Player'

        column, value = where.get('column'), where.get('value')
        operator = where.get('operator')
        condition = f'{column} {operator} {value}'

        return f'SELECT * FROM Player WHERE {condition}'

    @staticmethod
    def update_player(player_id, data):
        query = f'''
        UPDATE Player
        SET 
        '''
        for field, value in data.items():
            query += f'{field}={value},'

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
        print('Database connection successful')
    except Error as err:
        print(f"Error: '{err}'")

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
        print('Database connection successful')
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    """
    Create a new schema;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('DB schema created successfully')
    except Error as err:
        print(f"Error: '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query successful')
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def init_db():
    """
    Initial migration script;
    Creates the schema and tables.
    *Run this function only in the first execution of the system*
    """
    con = db_connection()

    # Creates main schema and tables
    script = (
        DBQueries.create_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DBQueries.use_schema(MYSQL_CONFIG['MYSQL_DATABASE']),
        DBQueries.create_player_table()
    )
    for statement in script:
        execute_query(con, statement)
    print('Database and tables created!')