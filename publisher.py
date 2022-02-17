from redis_connection import redis_connection
import sys

def send_message(name, message):
    client = redis_connection()
    client.publish(name, message)

    return "Done"


if __name__ == "__main__":
    program, channel_name, message = sys.argv


    results = send_message(name=channel_name, message=message)