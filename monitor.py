import requests
import time
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1378744766937698499/v2V1YYqck0WF-V0VIg25t5Qw1CjkGkj0br0ttvJ8PddmWgHaB1KhwN1eXB5ZHalpqabA"

KEYWORDS = [
    "nike dunks", "nike p-6000s", "nike air force 1",
    "nike reacts", "nike air max", "nike air max 95"
]

PRICE_LIMITS = {
    "nike air force 1": 10,
    "nike reacts": 10,
    "nike p-6000s": 20,
    "nike air max": 20,
    "nike air max 95": 20,
    "nike dunks": 20,
}

SIZES = list(range(39, 47))  # EU sizes roughly UK6–UK11.5
CONDITIONS = ["new_with_tags", "new_without_tags", "very_good"]
CHECK_INTERVAL = 30  # seconds

sent_ids = set()

def search_vinted(keyword):
    url = f"https://www.vinted.co.uk/api/v2/catalog/items"
    params = {
        "search_text": keyword,
        "size_id[]": SIZES,
        "status[]": CONDITIONS,
        "price_to": PRICE_LIMITS.get(keyword, 20),
        "currency": "GBP",
        "catalog[]": 5,
        "order": "newest_first",
        "page": 1
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        items = response.json().get("items", [])
        return items
    except Exception as e:
        print("Error fetching from Vinted:", e)
        return []

def send_to_discord(item):
    title = item["title"]
    price = item["price"]
    url = f'https://www.vinted.co.uk{item["url"]}'
    image = item["photo"]["url"]

    webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"**{title}** - £{price} \n{url}")
    webhook.add_file(file=requests.get(image).content, filename='image.jpg')
    webhook.execute()

def main():
    print("✅ Vinted monitor started.")
    while True:
        for keyword in KEYWORDS:
            items = search_vinted(keyword)
            for item in items:
                if item["id"] not in sent_ids:
                    send_to_discord(item)
                    sent_ids.add(item["id"])
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
