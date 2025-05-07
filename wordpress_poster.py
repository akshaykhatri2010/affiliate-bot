import json
import requests
import base64
import os

WORDPRESS_URL = os.getenv("WORDPRESS_URL")
USERNAME = os.getenv("WORDPRESS_USERNAME")
PASSWORD = os.getenv("WORDPRESS_PASSWORD")
FILES = ["grabon_deals.json", "cuelinks_offers.json", "posts.json"]

def post_to_wordpress(item, post_type="posts"):
    url = f"{WORDPRESS_URL}/wp-json/wp/v2/{post_type}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {base64.b64encode(f'{USERNAME}:{PASSWORD}'.encode()).decode()}"
    }
    data = {
        "title": item["title"],
        "content": f"{item['content']}<br>Keywords: {item['keywords']}",
        "status": "publish",
        "meta": {
            "yoast_wpseo_metadesc": item["keywords"],
            "yoast_wpseo_focuskw": item["keywords"].split(",")[0]
        }
    }
    if post_type == "rehub_offer":
        data["meta"].update({
            "rehub_offer_product_url": item["affiliate_link"],
            "rehub_offer_product_price": f"{item['discount']}%",
            "rehub_offer_btn_text": "Claim Deal"
        })
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        print(f"Posted: {item['title']}")
    except requests.RequestException as e:
        print(f"Error posting: {e}")

def process_files():
    for file in FILES:
        try:
            with open(file, "r") as f:
                for line in f:
                    item = json.loads(line.strip())
                    post_type = "rehub_offer" if item["post_type"] == "deal" else "posts"
                    post_to_wordpress(item, post_type)
        except FileNotFoundError:
            print(f"No data in {file}")

if __name__ == "__main__":
    process_files()
