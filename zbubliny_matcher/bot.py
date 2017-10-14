import os
import sys
import json

import click


import requests
from flask import Flask, request

app = Flask(__name__)
from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/bot', methods=['GET'])
def verify():
    print(request.args)
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["ZBUBLINY_FB_VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/bot', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)

    # endpoint for processing incoming messaging events
    # try:
    #     data = request.get_json()
    #     log(data)  # you may not want to log every incoming message in production, but it's good for testing
    #
    #     if data["object"] == "page":
    #
    #         for entry in data["entry"]:
    #             for messaging_event in entry["messaging"]:
    #
    #                 if messaging_event.get("message"):  # someone sent us a message
    #
    #                     sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
    #                     recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
    #                     try:
    #                         message_text = messaging_event["message"]["text"]  # the message's text
    #
    #                         reply=predict(message_text)
    #                         send_message(sender_id, str(reply))
    #                     except:
    #                         send_message(sender_id,str("Sorry! I didn't get that."))
    #                 if messaging_event.get("delivery"):  # delivery confirmation
    #                     pass
    #
    #                 if messaging_event.get("optin"):  # optin confirmation
    #                     pass
    #
    #                 if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
    #                     pass
    #
    #     return "ok", 200
    # except:
    return "ok", 200
#
def send_message(recipient_id, message_text):
    print("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
#
#
# def log(message):  # simple wrapper for logging to stdout on heroku
#     print str(message)
#     sys.stdout.flush()

# def predict(incoming_msg):
#    return predict_reply.classify(incoming_msg);


@click.command()
@click.option("-p", "--port", default=8888)
def run_server(port):
    app.run(debug=False, host="0.0.0.0", port=port)



if __name__ == '__main__':
    run_server()