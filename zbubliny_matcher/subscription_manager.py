from psycopg2 import connect
import os


class SubscriptionManager:
    def __init__(self, host=None, user=None, password=None, db=None):
        self.host = host or os.environ["ZBUBLINY_DB_HOST"]
        self.user = user or os.environ["ZBUBLINY_DB_USER"]
        self.password = password or os.environ["ZBUBLINY_DB_PASSWORD"]
        self.db = db or os.environ["ZBUBLINY_DB_DB"]
        self.cursor = None

    def get_cursor(self):
        if not self.cursor:
            dsn = "host={0} dbname={1} user={2} password={3}".format(self.host, self.db, self.user, self.password)
            connection = connect(dsn)
            self.cursor = connection.cursor()
        return self.cursor

    def subscribe(self, id, keyword):
        sql = "INSERT INTO subscription(fb_id, keyword) VALUES (%s, %s) ON CONFLICT DO NOTHING"
        cursor = self.get_cursor()
        cursor.execute(sql, (str(id), str(keyword)))
        cursor.connection.commit()

    def unsubscribe(self, id, keyword):
        sql = "DELETE FROM subscription WHERE fb_id=%s AND keyword=%s"
        cursor = self.get_cursor()
        cursor.execute(sql, (str(id), str(keyword)))
        cursor.connection.commit()

    def get_subscriptions(self):
        sql = "SELECT fb_id, keyword FROM subscription"
        cursor = self.get_cursor()
        cursor.execute(sql)
        return cursor.fetchall()
