import requests
import time
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK"
UPTIMEROBOT_PING_URL = ""  # Optional

KEYWORDS = [
    "nike dunks", "nike p-6000s", "nike air force 1", "nike reacts",
    "nike air max", "nike air max 95",
    "nike trainers", "nike jordan", "nike jordans", "nike shoes", "jordans", "jordan"
]

PRICE_LIMITS = {
    "nike air force 1": 10,
    "nike reacts": 10,
    "nike p-6000s": 20,
    "nike air max": 20,
    "nike air max 95": 20,
    "nike dunks": 20,
    "nike trainers": 20,
    "nike jordan": 20,
    "nike jordans": 20,
    "nike shoes": 20,
    "jordans": 20,
    "jordan": 20
}

SIZES = list(range(39, 47))  # EU sizes ~ UK6 to UK11.5
CONDITIONS = ["new_with_tags", "new_without_tags", "very_good"]
CHECK_INTERVAL = 30  # seconds

sent_ids = set()

def search_vinted(keyword, page=1):
    url = "https://www.vinted.co.uk/api/v2/catalog/items"
    params = {
        "search_text": keyword,
        "size_id[]": SIZES,
        "status[]": CONDITIONS,
        "price_to": PRICE_LIMITS.get(keyword, 20),
        "currency": "GBP",
        "catalog[]": 5,
        "order": "newest_first",
        "page": page
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.vinted.co.uk/",
        "Origin": "https://www.vinted.co.uk"
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print(f"⚠️ Vinted returned {response.status_code}: {response.text[:200]}")
        return []
    return response.json().get("items", [])

def send_to_discord(item):
    item_id = item["id"]
    if item_id in sent_ids:
        return
    sent_ids.add(item_id)

    title = item["title"]
    price = item["price"]
    url = f"https://www.vinted.co.uk{item['url']}"
    photo = item["photo"]["url"]

    print(f"✅ Found: {title} - £{price} - {url}")

    webhook = DiscordWebhook(
        url=WEBHOOK_URL,
        content=f"**{title}** - £{price}\n{url}",
        username="Vinted Monitor",
        avatar_url=photo
    )
    webhook.execute()

def main():
    while True:
        try:
            for keyword in KEYWORDS:
                items = search_vinted(keyword)
                for item in items:
                    send_to_discord(item)

            if UPTIMEROBOT_PING_URL:
                requests.get(UPTIMEROBOT_PING_URL)

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
