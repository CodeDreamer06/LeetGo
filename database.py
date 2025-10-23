import sqlite3
import logging

logger = logging.getLogger('LeetGo')


class Database:
    """Provides a connection to a sqlite3 database"""

    def __init__(self):
        """Initializes sqlite and creates the necessary tables if they don't exist"""
        try:
            self.connection = sqlite3.connect('storage.db')
            self.c = self.connection.cursor()
            
            # Create cohorts table
            self.c.execute(
                'CREATE TABLE IF NOT EXISTS cohorts(cohort_id INTEGER PRIMARY KEY, name TEXT)')
            
            # Create users table
            self.c.execute('''CREATE TABLE IF NOT EXISTS users(
                      user_id INTEGER PRIMARY KEY NOT NULL,
                      cohort_id INTEGER,
                      discord_username TEXT NOT NULL UNIQUE,
                      lc_username TEXT,
                      roadmap TEXT,
                      goal_questions INTEGER,
                      goal_duration INTEGER,
                      goal_start_date TEXT,
                      reminder_hour INTEGER,
                      reminder_minute INTEGER,
                      FOREIGN KEY(cohort_id) REFERENCES cohorts(cohort_id))''')
            
            self.connection.commit()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise

    def does_the_user_exist(self, discord_username) -> bool:
        """Checks if the user exists in the database"""
        try:
            return self.c.execute('SELECT * FROM users WHERE discord_username=?',
                                  (discord_username,)).fetchone() is not None
        except Exception as e:
            logger.error(f"Error checking if user exists: {e}")
            return False

    def change_user_name(self, discord_username, lc_username):
        """Changes the user's name in the database"""
        try:
            self.c.execute('UPDATE users SET lc_username=? WHERE discord_username=?',
                           (lc_username, discord_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error changing username: {e}")
            raise

    def add_user(self, discord_username, lc_username):
        """Adds a user to the database"""
        try:
            self.c.execute('INSERT INTO users (discord_username, lc_username) VALUES (?, ?)',
                           (discord_username, lc_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error adding user: {e}")
            raise

    def find_user(self, discord_username) -> str:
        """Fetches leetcode username from the database"""
        try:
            user = self.c.execute('SELECT lc_username FROM users WHERE discord_username=?',
                                  (discord_username,)).fetchone()
            if user:
                return user[0]
            else:
                return None
        except Exception as e:
            logger.error(f"Error finding user: {e}")
            return None

    def get_all_cohorts(self) -> list:
        """Fetches all cohorts from the database"""
        try:
            return self.c.execute('SELECT * FROM cohorts').fetchall()
        except Exception as e:
            logger.error(f"Error fetching cohorts: {e}")
            return []

    def get_user_cohort(self, discord_username: str) -> int:
        """Fetches user's cohort id from the database"""
        try:
            row = self.c.execute('SELECT cohort_id FROM users WHERE discord_username=?',
                                    (discord_username,)).fetchone()
            if not row or row[0] is None:
                return None
            return int(row[0])
        except Exception as e:
            logger.error(f"Error fetching user cohort: {e}")
            return None

    def create_cohort(self, cohort_name: str, host_discord_name: str):
        """Lets a user to host a cohort"""
        try:
            self.c.execute('INSERT INTO cohorts (name) VALUES (?)', (cohort_name,))
            cohort_id = int(self.c.execute(
                'SELECT cohort_id FROM cohorts WHERE name=?', (cohort_name, )).fetchone()[0])
            self.update_user_cohort(host_discord_name, cohort_id)
        except Exception as e:
            logger.error(f"Error creating cohort: {e}")
            raise

    def update_user_cohort(self, discord_username, cohort_id):
        """Updates user's cohort in the database"""
        try:
            self.c.execute('UPDATE users SET cohort_id=? WHERE discord_username=?',
                           (cohort_id, discord_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error updating user cohort: {e}")
            raise

    def get_cohort_name(self, cohort_id: int) -> str:
        """Fetches cohort name from the database"""
        try:
            row = self.c.execute('SELECT name FROM cohorts WHERE cohort_id=?',
                                (cohort_id,)).fetchone()
            if row:
                return row[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching cohort name: {e}")
            return None

    def remove_user_from_cohort(self, discord_username: str):
        """Removes user from their current cohort"""
        try:
            self.c.execute('UPDATE users SET cohort_id=NULL WHERE discord_username=?',
                           (discord_username,))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error removing user from cohort: {e}")
            raise

    def set_user_roadmap(self, discord_username: str, roadmap: str):
        """Sets user's learning roadmap"""
        try:
            self.c.execute('UPDATE users SET roadmap=? WHERE discord_username=?',
                           (roadmap, discord_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error setting user roadmap: {e}")
            raise

    def get_user_roadmap(self, discord_username: str) -> str:
        """Fetches user's roadmap from the database"""
        try:
            row = self.c.execute('SELECT roadmap FROM users WHERE discord_username=?',
                                (discord_username,)).fetchone()
            if row:
                return row[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user roadmap: {e}")
            return None

    def set_user_goal(self, discord_username: str, questions: int, months: int, start_date: str):
        """Sets user's goal"""
        try:
            self.c.execute('''UPDATE users SET goal_questions=?, goal_duration=?, goal_start_date=? 
                           WHERE discord_username=?''',
                           (questions, months, start_date, discord_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error setting user goal: {e}")
            raise

    def get_user_goal(self, discord_username: str) -> tuple:
        """Fetches user's goal from the database"""
        try:
            row = self.c.execute('''SELECT goal_questions, goal_duration, goal_start_date 
                                 FROM users WHERE discord_username=?''',
                                (discord_username,)).fetchone()
            if row and row[0] is not None:
                return row
            return None
        except Exception as e:
            logger.error(f"Error fetching user goal: {e}")
            return None

    def set_user_reminder(self, discord_username: str, hour: int, minute: int):
        """Sets user's reminder time"""
        try:
            self.c.execute('UPDATE users SET reminder_hour=?, reminder_minute=? WHERE discord_username=?',
                           (hour, minute, discord_username))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error setting user reminder: {e}")
            raise

    def get_user_reminder(self, discord_username: str) -> tuple:
        """Fetches user's reminder time from the database"""
        try:
            row = self.c.execute('SELECT reminder_hour, reminder_minute FROM users WHERE discord_username=?',
                                (discord_username,)).fetchone()
            if row and row[0] is not None:
                return row
            return None
        except Exception as e:
            logger.error(f"Error fetching user reminder: {e}")
            return None

    def remove_user_reminder(self, discord_username: str):
        """Removes user's reminder"""
        try:
            self.c.execute('UPDATE users SET reminder_hour=NULL, reminder_minute=NULL WHERE discord_username=?',
                           (discord_username,))
            self.connection.commit()
        except Exception as e:
            logger.error(f"Error removing user reminder: {e}")
            raise

    def get_users_with_reminder_time(self, hour: int, minute: int) -> list:
        """Fetches all users with reminders set for a specific time"""
        try:
            rows = self.c.execute('''SELECT discord_username FROM users 
                                  WHERE reminder_hour=? AND reminder_minute=?''',
                                 (hour, minute)).fetchall()
            return [row[0] for row in rows]
        except Exception as e:
            logger.error(f"Error fetching users with reminder time: {e}")
            return []

    def kill(self):
        """Safely closes the sqlite connection before the instance of the class is removed"""
        try:
            self.connection.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")
