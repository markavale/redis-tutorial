from redis_connection import redis_connection
import sys
from bs4 import BeautifulSoup
from requests import request

def get_message_from_publisher(name):
    client = redis_connection()
    client_pubsub = client.pubsub()
    client_pubsub.subscribe(name)

    while True:
        message_from_publisher = client_pubsub.get_message()
        if message_from_publisher and not message_from_publisher['data'] == 1:
            message = message_from_publisher['data']
            scraped_data = scrape(message)
            if scraped_data is not None:
                print("ARTICLE SCRAPED:", scraped_data)
                new_client = redis_connection()
                new_client.publish("exporter", scraped_data)

    return "Done"

def scrape(url: str) -> str:
    res = request(method="GET", url=url)
    if res.status_code == 200:
        page_source = res.text
        soup = BeautifulSoup(page_source, "html.parser")
        og_meta_title = soup.find("meta", {"property": "og:title"})
        if og_meta_title is not None:
            return og_meta_title.get("content", "No title")
    else:
        print(f"Status code of {res.status_code}")
        return None

def is_palindrome(text: str) -> bool:
    return True if text == text[::-1] else False

if __name__ == "__main__":
    channel_name = sys.argv[1]

    results = get_message_from_publisher(name=channel_name)
