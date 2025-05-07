import requests
import json
import time
from bs4 import BeautifulSoup

DEALS_PER_DAY = 2
D2C_BRANDS = ["boAt", "Mamaearth", "Licious", "Bewakoof", "Sugar Cosmetics"]

def scrape_grabon_deals():
    url = "https://www.grabon.in/all-coupons/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        deal_cards = soup.find_all("div", class_="coupon-card")
        deals = []
        for card in deal_cards:
            title_elem = card.find("h3", class_="coupon-title")
            description_elem = card.find("p", class_="coupon-description")
            link_elem = card.find("a", class_="coupon-link")
            if title_elem and description_elem and link_elem:
                title = title_elem.text.strip()
                description = description_elem.text.strip()
                link = link_elem["href"]
                if any(brand.lower() in title.lower() for brand in D2C_BRANDS):
                    brand = next((b for b in D2C_BRANDS if b.lower() in title.lower()), "D2C")
                    deals.append({
                        "title": f"{brand} Deal: {title}",
                        "content": description,
                        "affiliate_link": link,
                        "discount": "N/A",
                        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "post_type": "deal",
                        "keywords": f"{brand} deals 2025, {brand.lower()} coupon, best {brand.lower()} offers"
                    })
        for deal in deals[:DEALS_PER_DAY]:
            with open("grabon_deals.json", "a") as f:
                json.dump(deal, f)
                f.write("\n")
            print(f"Scraped deal: {deal['title']}")
    except requests.RequestException as e:
        print(f"Error scraping GrabOn: {e}")

if __name__ == "__main__":
    scrape_grabon_deals()
