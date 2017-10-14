import json
import time
import boto3
import click


class MessageDemon:
    def __init__(self):
        self.sqs = boto3.resource('sqs')
        self.queue = self.sqs.get_queue_by_name(QueueName='news-stream')

    def run(self):
        while True:
            for message in self.queue.receive_messages():
                data = json.loads(message.body)
                print(data)
                self.process_message(data)
                message.delete()
            time.sleep(1)

    def process_message(self, message):
        pass


@click.command()
def run():
    md = MessageDemon()
    md.run()


if __name__ == "__main__":
    run()


