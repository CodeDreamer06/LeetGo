import sqlite3


class Database:
    """Provides a connection to a sqlite3 database"""

    def __init__(self):
        """Initializes sqlite and creates the necessary tables if they don't exist"""
        self.connection = sqlite3.connect('storage.db')
        self.c = self.connection.cursor()
        self.c.execute(
            'CREATE TABLE IF NOT EXISTS cohorts(cohort_id INTEGER PRIMARY KEY, name TEXT)')
        self.c.execute('''CREATE TABLE IF NOT EXISTS users(
                  user_id INTEGER PRIMARY KEY NOT NULL,
                  cohort_id INTEGER,
                  discord_username TEXT NOT NULL,
                  lc_username TEXT,
                  roadmap INTEGER,
                  goal_questions INTEGER,
                  goal_duration INTEGER,
                  goal_start_date TEXT,
                  FOREIGN KEY(cohort_id) REFERENCES cohorts(cohort_id))''')

    def does_the_user_exist(self, discord_username) -> bool:
        """Checks if the user exists in the database"""
        return self.c.execute('SELECT * FROM users WHERE discord_username=?',
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

    def get_all_cohorts(self) -> list:
        """Fetches all cohorts from the database"""
        return self.c.execute('SELECT * FROM cohorts').fetchall()

    def get_user_cohort(self, discord_username: str) -> int:
        """Fetches user's cohort id from the database"""
        row = self.c.execute('SELECT cohort_id FROM users WHERE discord_username=?',
                                (discord_username,)).fetchone()
        if not row or row[0] is None:
            return None
        return int(row[0])

    def create_cohort(self, cohort_name: str, host_discord_name: str):
        """Lets a user to host a cohort"""
        self.c.execute('INSERT INTO cohorts (name) VALUES (?)', (cohort_name,))
        cohort_id = int(self.c.execute(
            'SELECT cohort_id FROM cohorts WHERE name=?', (cohort_name, )).fetchone()[0])
        self.update_user_cohort(host_discord_name, cohort_id)

    def update_user_cohort(self, discord_username, cohort_id):
        """Updates user's cohort in the database"""
        self.c.execute('UPDATE users SET cohort_id=? WHERE discord_username=?',
                       (cohort_id, discord_username))
        self.connection.commit()

    def kill(self):
        """Safely closes the sqlite connection before the instance of the class is removed"""
        self.connection.close()
