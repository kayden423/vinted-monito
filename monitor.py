import requests
import time
from discord_webhook import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/1378744766937698499/v2V1YYqck0WF-V0VIg25t5Qw1CjkGkj0br0ttvJ8PddmWgHaB1KhwN1eXB5ZHalpqabA"
UPTIMEROBOT_PING_URL = ""  # Optional: paste your UptimeRobot ping URL here if you have one

KEYWORDS = [
    "nike dunks", "nike p-6000s", "nike air force 1", "nike reacts",
    "nike air max", "nike air max 95", "nike trainers", "nike jordan",
    "nike jordans", "nike shoes", "jordans", "jordan"
]

PRICE_LIMITS = {
    "nike air force 1": 15,
    "nike reacts": 15,
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
        "price_to": PRICE_LIMITS.get(key
