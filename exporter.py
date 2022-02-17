from distutils.command.clean import clean
from redis_connection import redis_connection
import sys

def listen(channel_name):
    client = redis_connection()
    client_pubsub = client.pubsub()
    client_pubsub.subscribe(channel_name)

    while True:
        message_from_publisher = client_pubsub.get_message()
        if message_from_publisher and not message_from_publisher['data'] == 1:
            message = message_from_publisher['data']
            export_file(message)


def export_file(mesage: str):
    with open("export_data.txt", "a") as file_append:
        print(f"{mesage} exported")
        file_append.write(str(mesage)+"\n")



if __name__ == "__main__":
    channel_name = sys.argv[1]

    listen(channel_name)

