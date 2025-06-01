import requests
import time

# CONFIGURATION
WEBHOOK_URL = "https://discord.com/api/webhooks/1378744766937698499/v2V1YYqck0WF-V0VIg25t5Qw1CjkGkj0br0ttvJ8PddmWgHaB1KhwN1eXB5ZHalpqabA"
KEYWORDS = [
    "nike dunks", "nike p-6000", "nike air force 1", 
    "nike reacts", "nike air max", "nike air max 95"
]
SIZES = [39, 40, 41, 42, 43, 44, 45, 46]  # EU sizes
CONDITIONS = ["new_with_tags", "new_without_tags", "very_good_condition"]
MAX_PRICES = {
    "nike air force 1": 10,
    "nike reacts": 10,
    "nike p-6000": 20,
    "nike air max": 20,
    "nike air max 95": 20,
    "nike dunks": 20
}

SEEN_IDS = set()

def send_to_discord(item):
    title = item["title"]
    url = f'https://www.vinted.co.uk{item["url"]}'
    price = item["price"]
    size = item["size_title"]
    image_url = item["photo"]["url"]

    data = {
        "content": None,
        "embeds": [{
            "title": title,
            "url": url,
            "color": 16777215,
            "fields": [
                {"name": "Price", "value": f"£{price}", "inline": True},
                {"name": "Size", "value": size, "inline": True}
            ],
            "thumbnail": {"url": image_url}
        }]
    }

    requests.post(WEBHOOK_URL, json=data)

def check_vinted():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }
    for keyword in KEYWORDS:
        query = keyword.replace(" ", "%20")
        url = f"https://www.vinted.co.uk/api/v2/catalog/items?search_text={query}&order=newest_first&per_page=20"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 403:
                print("❌ Vinted blocked the request (403).")
                continue
            items = response.json()["items"]
            for item in items:
                item_id = item["id"]
                if item_id in SEEN_IDS:
                    continue
                SEEN_IDS.add(item_id)

                size = item.get("size_id")
                condition = item.get("item_condition")
                price = float(item["price"])

                if size not in SIZES or condition not in CONDITIONS:
                    continue

                for keyword_key in MAX_PRICES:
                    if keyword_key in item["title"].lower():
                        if price <= MAX_PRICES[keyword_key]:
                            send_to_discord(item)
                        break

        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    while True:
        check_vinted()
        time.sleep(60)
