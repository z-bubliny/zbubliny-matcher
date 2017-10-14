from psycopg2 import connect
import os
from .matchers import SimpleMatcher


class DatabaseScanner:
    def __init__(self, host=None, user=None, password=None, db=None, matcher=SimpleMatcher()):
        self.host = host or os.environ["ZBUBLINY_DB_HOST"]
        self.user = user or os.environ["ZBUBLINY_DB_USER"]
        self.password = password or os.environ["ZBUBLINY_DB_PASSWORD"]
        self.db = db or os.environ["ZBUBLINY_DB_DB"]
        self.cursor = None
        self.matcher = matcher

    def get_cursor(self):
        if not self.cursor:
            dsn = "host={0} dbname={1} user={2} password={3}".format(self.host, self.db, self.user, self.password)
            connection = connect(dsn)
            self.cursor = connection.cursor()
        return self.cursor

    def fetch_articles(self):
        query = "SELECT language, title, body, source FROM good_article"
        cursor = self.get_cursor()
        cursor.execute(query)
        return ({
            "language": row[0],
            "title": row[1],
            "body": row[2],
            "source": row[3]
        } for row in cursor.fetchall())

    def search_keyword(self, keyword, keyword_language):
        for article in self.fetch_articles():
            pass



