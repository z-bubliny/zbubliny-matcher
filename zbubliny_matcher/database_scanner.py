from psycopg2 import connect
import os
import click

from .matchers import SimpleMatcher
from .site_trustworthiness import WOT_API


class DatabaseScanner:
    def __init__(self, host=None, user=None, password=None, db=None, matcher=SimpleMatcher(), all=False):
        self.host = host or os.environ["ZBUBLINY_DB_HOST"]
        self.user = user or os.environ["ZBUBLINY_DB_USER"]
        self.password = password or os.environ["ZBUBLINY_DB_PASSWORD"]
        self.db = db or os.environ["ZBUBLINY_DB_DB"]
        self.all = all
        self.cursor = None
        self.matcher = matcher
        self.threshold = 0.8

    def get_cursor(self):
        if not self.cursor:
            dsn = "host={0} dbname={1} user={2} password={3}".format(self.host, self.db, self.user, self.password)
            connection = connect(dsn)
            self.cursor = connection.cursor()
        return self.cursor

    @property
    def table_name(self):
        return "each_article" if self.all else "good_article"

    def fetch_articles(self):
        query = "SELECT language, title, body, source FROM {0}".format(self.table_name)
        print(query)
        cursor = self.get_cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        while row:
            yield {
                "language": row[0],
                "title": row[1],
                "body": row[2],
                "source": row[3]
            }
            row = cursor.fetchone()

    def search_keywords(self, keywords, keyword_language, limit=1000000):
        checked = set()
        found = 0
        for article in self.fetch_articles():
            if article["source"] in checked:
                continue
            checked.add(article["source"])
            relevance = self.matcher(article["title"] + article["body"], keywords, article["language"] or "en", keyword_language)
            if relevance > self.threshold:
                yield article, relevance
                found += 1
            if found >= limit:
                return


@click.command()
@click.option("-l", "--language", default="cs")
@click.option("-a", "--all", is_flag=True)
@click.option("-t", "--trustworthiness", is_flag=True)
# @click.option("-")
@click.argument("keywords", nargs=-1)
def run_scanner(keywords, language, trustworthiness, all):
    ds = DatabaseScanner(all=all)
    for article, relevance in ds.search_keywords(keywords, keyword_language=language):
        if trustworthiness:
            nice = WOT_API.get_trustworthiness(article["source"])
            print("* {0} {1} [{2} %]".format(article["title"], article["source"], nice))
        else:
            print("* {0} {1}".format(article["title"], article["source"]))