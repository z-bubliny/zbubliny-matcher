import click
import json
import time
from flask import Flask, jsonify, Response, request

from .database_scanner import DatabaseScanner

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def get_search():
    keywords = request.args.get("keywords")
    language = request.args.get("lang", "cs")
    if keywords:
        keywords = keywords.split(",")
        ds = DatabaseScanner(all=all)

        def generate():
            yield "KEYWORDS: `{0}`\n".format(keywords)
            yield "LANGUAGE: `{0}`\n".format(language)

            for row in ds.search_keywords(keywords, language):
                article, relevance = row
                data = {val : article[val] for val in ("title", "source")}
                data["relevance"] = relevance
                yield json.dumps(data) + '\n'
                time.sleep(1)

        return Response(generate(), mimetype='text/plain')

    else:
        return "?keywords=...,...,...", 400


@click.command()
def run_server():
    app.run(debug=True)

if __name__ == '__main__':
    run_server()
