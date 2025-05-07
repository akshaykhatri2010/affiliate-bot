import requests
import json
import time
import os

API_KEY = os.getenv("CUELINKS_API_KEY")
DEALS_PER_DAY = 3
D2C_BRANDS = ["boAt", "Mamaearth", "Licious", "Bewakoof", "Sugar Cosmetics"]

def fetch_cuelinks_offers():
    url = f"https://www.cuelinks.com/api/v1/offers?api_key={API_KEY}&country=IN&limit={DEALS_PER_DAY}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        offers = response.json().get("offers", [])
        filtered_offers = [
            offer for offer in offers
            if any(brand.lower() in offer.get("merchant", "").lower() for brand in D2C_BRANDS)
        ]
        for offer in filtered_offers[:DEALS_PER_DAY]:
            brand = next((b for b in D2C_BRANDS if b.lower() in offer.get("merchant", "").lower()), "D2C")
            item = {
                "title": f"{brand} Offer: {offer.get('title', 'D2C Deal')}",
                "content": f"Grab {offer.get('discount_percentage', 'up to 50')}% off on {offer.get('merchant', 'this brand')}!",
                "affiliate_link": offer.get("url"),
                "discount": offer.get("discount_percentage", "N/A"),
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "post_type": "deal",
                "keywords": f"{brand} offers 2025, {brand.lower()} discount, best {brand.lower()} deals"
            }
            with open("cuelinks_offers.json", "a") as f:
                json.dump(item, f)
                f.write("\n")
            print(f"Fetched offer: {item['title']}")
    except requests.RequestException as e:
        print(f"Error fetching Cuelinks: {e}")

if __name__ == "__main__":
    fetch_cuelinks_offers()
