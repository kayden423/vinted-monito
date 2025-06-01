import requests
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from discord_webhook import DiscordWebhook, DiscordEmbed

# === Discord Webhook ===
WEBHOOK_URL = "https://discord.com/api/webhooks/1378744766937698499/v2V1YYqck0WF-V0VIg25t5Qw1CjkGkj0br0ttvJ8PddmWgHaB1KhwN1eXB5ZHalpqabA"

# === Keywords & Filters ===
KEYWORDS = [
    "nike dunks", "nike p-6000s", "nike air force 1",
    "nike reacts", "nike air max", "nike air max 95",
    "nike trainers", "nike jordan", "nike jordans",
    "nike shoes", "jordans", "jordan"
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

SIZES = list(range(39, 47))  # EU sizes ≈ UK6–UK11.5
CONDITIONS = ["new_with_tags", "new_without_tags", "very_good"]
CHECK_INTERVAL = 30  # seconds
PAGES_TO_CHECK = 3   # Check first 3 pages of Vinted results

# === Duplicate ID Protection ===
def load_sent_ids():
    try:
        with open("sent_ids.txt", "r") as f:
            return set(map(int, f.read().splitlines()))
    except:
        return set()

def save_sent_id(item_id):
    with open("sent_ids.txt", "a") as f:
        f.write(f"{item_id}\n")

sent_ids = load_sent_ids()

# === Vinted Search ===
def search_vinted(keyword, page):
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
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        items = response.json().get("items", [])
        return items
    except Exception as e:
        print("❌ Error fetching from Vinted:", e)
        return []

# === Discord Send ===
def send_to_discord(item):
    title = item["title"]
    price = item["price"]
    url = f'https://www.vinted.co.uk{item["url"]}'
    image = item["photo"]["url"] if item.get("photo") else None

    webhook = DiscordWebhook(url=WEBHOOK_URL)
    embed = DiscordEmbed(title=title, url=url, color="242424")
    embed.add_embed_field(name="Price", value=f"£{price}")
    embed.set_footer(text="Vinted Monitor")
    if image:
        embed.set_thumbnail(url=image)

    webhook.add_embed(embed)
    webhook.execute()

# === Monitor Loop ===
def monitor_loop():
    print("✅ Vinted monitor started.")
    while True:
        for keyword in KEYWORDS:
            for page in range(1, PAGES_TO_CHECK + 1):
                items = search_vinted(keyword, page)
                for item in items:
                    if item["id"] not in sent_ids:
                        print(f"👟 {keyword} | Found: {item['title']} - £{item['price']} — Sending")
                        send_to_discord(item)
                        sent_ids.add(item["id"])
                        save_sent_id(item["id"])
        time.sleep(CHECK_INTERVAL)

# === UptimeRobot Ping Server ===
class PingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'✅ Vinted Monitor is running.')

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), PingHandler)
    print("🌐 Ping server running on port 8080...")
    server.serve_forever()

# === Run Everything ===
if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    monitor_loop()
