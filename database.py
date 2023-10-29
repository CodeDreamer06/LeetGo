import sqlite3


class Database:
    """Provides a connection to a sqlite3 database"""

    def __init__(self):
        """Initializes sqlite and creates the necessary tables if they don't exist"""
        connection = sqlite3.connect('storage.db')
        c = connection.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS cohorts(id INTEGER PRIMARY KEY, name TEXT)')
        # FIXME: sqlite3.OperationalError: near "FOREIGN": syntax error
        c.execute('''CREATE TABLE IF NOT EXISTS users(
                  id INTEGER PRIMARY KEY NOT NULL,
                  cohort REFERENCES cohorts(id) INTEGER,
                  discord_username TEXT NOT NULL,
                  lc_username TEXT,
                  roadmap INTEGER,
                  goal_questions INTEGER,
                  goal_duration INTEGER,
                  goal_start_date TEXT)''')

    def does_the_user_exist(self, discord_username) -> bool:
        """Checks if the user exists in the database"""
        self.c.execute('SELECT * FROM users WHERE discord_username=?',
                       (discord_username,)).fetchone()

    def change_user_name(self, discord_username, lc_username):
        """Changes the user's name in the database"""
        self.c.execute('UPDATE users SET lc_username=? WHERE discord_username=?',
                       (lc_username, discord_username))
        self.connection.commit()

    def add_user(self, discord_username, lc_username):
        """Adds a user to the database"""
        self.c.execute('INSERT INTO users (discord_username, lc_username) VALUES (?, ?)',
                       (discord_username, lc_username))
        self.connection.commit()

    def find_user(self, discord_username) -> str:
        """Fetches leetcode username from the database"""
        user = self.c.execute('SELECT lc_username FROM users WHERE discord_username=?',
                              (discord_username,)).fetchone()
        if user:
            return user[0]
        else:
            return None

    def get_all_cohorts(self):
        # TODO: Define return data type
        """Fetches all cohorts from the database"""
        return self.c.execute('SELECT * FROM cohorts')

    def update_user_cohort(self, discord_username, cohort_id):
        """Updates user's cohort in the database"""
        self.c.execute('UPDATE users SET cohort=? WHERE discord_username=?',
                       (cohort_id, discord_username))
        self.connection.commit()

    def kill(self):
        """Safely closes the sqlite connection before the instance of the class is removed"""
        self.connection.close()
