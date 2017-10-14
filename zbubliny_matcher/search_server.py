import click
import json
import time
from flask import Flask, jsonify, Response, request

from .database_scanner import DatabaseScanner

app = Flask(__name__)


@app.route('/api/search/', methods=['GET'])
def get_search():
    keywords = request.args.get("keywords")
    language = request.args.get("lang", "cs")
    count = int(request.args.get("count", 5))
    all = request.args.get("all", False)
    if keywords:
        keywords = keywords.split(",")
        ds = DatabaseScanner(all=all)

        results = []
        for i, row in enumerate(ds.search_keywords(keywords, language)):
            article, relevance = row
            data = {val : article[val] for val in ("title", "source")}
            data["relevance"] = relevance
            results.append(data)
            if i >= count:
                break

        response = Response(json.dumps(results), mimetype='text/json')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    else:
        return "Please add valid query string ?keywords=...,...,...", 400


@click.command()
@click.option("-p", "--public-ip", is_flag=True)
@click.option("-n", "--port-number", default=5000)
def run_server(public_ip, port_number):
    if public_ip:
        app.run(host = '0.0.0.0', debug=False, port=port_number)
    else:
        app.run(debug=True, port=port_number)


if __name__ == '__main__':
    run_server()
