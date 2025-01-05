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
    
    def close(self):
        """
        Close the database connection.
        """
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db = TweetDatabase()

    # Simulated tweet data
    tweet_data = {
        "tweet_id": "1874057709466902637",
        "username": "@mdvx_test",
        "content": "@MadivalVoyage\n hey, how are you?",
        "created_at": "2024-12-31T11:39:10.000Z",
        "href": "https://x.com/mdvx_test/status/1874057709466902637"
    }

    # Save the tweet
    db.save_tweet(
        tweet_data["tweet_id"],
        tweet_data["username"],
        tweet_data["content"],
        tweet_data["created_at"],
        tweet_data["href"]
    )

    # Simulated response data
    response_data = {
        "tweet_id": "1874057709466902637",  # This must match an existing tweet ID
        "response_content": "This is a response to the sample tweet.",
        "response_video": '''C:\\Users\\Alfian\\AppData\\Local\\Temp\\gradio\\8f54fafe71e36370d8e258df80931ca42aa0561b926f729c0ac7c773a66e7e65\\20250101_163450.mp4''',
        "response_created_at": "2024-12-31T12:30:00"
    }

    # Save the response
    db.save_response(
        response_data["tweet_id"],
        response_data["response_content"],
        response_data["response_video"],
        response_data["response_created_at"]
    )

    db.save_automated_tweet(
        response_data["response_content"],
        response_data["response_video"],
        response_data["response_created_at"]
    )

    # Close the connection
    db.close()
