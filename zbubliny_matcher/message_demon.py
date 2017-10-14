import json
import time
import boto3
import click

from .matchers import SimpleMatcher
from .subscription_manager import SubscriptionManager
from .bot import send_message


class MessageDemon:
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.queue = self.sqs.get_queue_by_name(QueueName='news-stream')
        self.manager = SubscriptionManager()
        self.matcher = SimpleMatcher()

    def run(self):
        while True:
            for message in self.queue.receive_messages():
                data = json.loads(message.body)
                print(data)
                self.process_message(data)
                message.delete()
            time.sleep(1)

    def process_message(self, message):
        id, source, title, text, image_url = message
        subscriptions = self.manager.get_subscriptions()
        print("Processing {0}...".format(title))
        for fb_id, keyword in subscriptions:
            quality = self.matcher(title + text, [keyword], text_language="en", keyword_language="cs")
            if quality:
                print("Matched: {0}, sending to {1}".format(keyword, fb_id))
                reply = "{0} : {1}\n\n".format(title, source)
                try:
                    send_message(fb_id, reply)
                except BaseException as be:
                    print("Error: {0}".format(be))
                    pass


@click.command()
def run():
    md = MessageDemon()
    md.run()


if __name__ == "__main__":
    run()


