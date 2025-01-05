import sqlite3

class TweetDatabase:
    def __init__(self, db_name="tweets.db"):
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the tweets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                tweet_id TEXT PRIMARY KEY,
                username TEXT,
                content TEXT,
                created_at TEXT,
                href TEXT
            )
        ''')

        # Create the responses table with a foreign key to the tweets table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS responses (
                response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                tweet_id TEXT,
                response_content TEXT,
                response_video TEXT,
                response_created_at TEXT,
                FOREIGN KEY (tweet_id) REFERENCES tweets(tweet_id)
            )
        ''')
        self.conn.commit()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS automated_tweets (
                automated_response_id INTEGER PRIMARY KEY AUTOINCREMENT,
                response_content TEXT,
                response_video TEXT,
                response_created_at TEXT
            )
        ''')
        self.conn.commit()

    def check_if_exist(self, tweet_id):
        # Check if the tweet already exists
        self.cursor.execute('SELECT tweet_id FROM tweets WHERE tweet_id = ?', (tweet_id,))
        result = self.cursor.fetchone()

        twt = False
        if result:
            print(f"Tweet with ID {tweet_id} already exists in the database.")
            twt = True

        self.cursor.execute('''
            SELECT response_id FROM responses WHERE tweet_id = ?
        ''', (tweet_id,))
        response_result = self.cursor.fetchone()
        
        resp = False
        if response_result:
            print(f"Response to tweet ID {tweet_id} already exists in the database.")
            resp = True
        
        if twt and resp:
            return True
        return False
        
    def save_tweet(self, tweet_id, username, content, created_at, href):
        """
        Save a tweet to the database if it doesn't already exist.
        """
        # Check if the tweet already exists
        self.cursor.execute('SELECT tweet_id FROM tweets WHERE tweet_id = ?', (tweet_id,))
        result = self.cursor.fetchone()

        if result:
            print(f"Tweet with ID {tweet_id} already exists in the database.")
            return False
        else:
            # Insert the tweet into the database
            self.cursor.execute('''
                INSERT INTO tweets (tweet_id, username, content, created_at, href)
                VALUES (?, ?, ?, ?, ?)
            ''', (tweet_id, username, content, created_at, href))
            self.conn.commit()
            print(f"Tweet with ID {tweet_id} added to the database.")
            return True

    def save_response(self, tweet_id, response_content, response_video, response_created_at):
        """
        Save a response to a tweet in the database.
        """
        # Check if the parent tweet exists
        self.cursor.execute('SELECT tweet_id FROM tweets WHERE tweet_id = ?', (tweet_id,))
        result = self.cursor.fetchone()

        if not result:
            print(f"Parent tweet with ID {tweet_id} does not exist in the database. Cannot save response.")
            return False

        # Check if the response already exists
        self.cursor.execute('''
            SELECT response_id FROM responses WHERE tweet_id = ?
        ''', (tweet_id,))
        response_result = self.cursor.fetchone()

        if response_result:
            print(f"Response to tweet ID {tweet_id} already exists in the database.")
            return False

        # Insert the response into the responses table
        self.cursor.execute('''
            INSERT INTO responses (tweet_id, response_content, response_video, response_created_at)
            VALUES (?, ?, ?, ?)
        ''', (tweet_id, response_content, response_video, response_created_at))
        self.conn.commit()
        print(f"Response to tweet ID {tweet_id} added to the database.")
        return True

    def save_automated_tweet(self, response_content, response_video, response_created_at):
        """
        Save a response to a tweet in the database.
        """

        # Insert the response into the responses table
        self.cursor.execute('''
            INSERT INTO automated_tweets (response_content, response_video, response_created_at)
            VALUES (?, ?, ?)
        ''', (response_content, response_video, response_created_at))
        self.conn.commit()
        print(f"Response automated tweet response added to the database.")
        return True
    
    def count_tweets_in_one_day(self, date):
        """
        Count the number of tweets created on a specific date.
        """
        self.cursor.execute('''
            SELECT COUNT(*) FROM tweets WHERE DATE(created_at) = ?
        ''', (date,))
        count = self.cursor.fetchone()[0]
        print(f"Number of tweets on {date}: {count}")
        return count

    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()