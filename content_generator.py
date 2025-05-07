import requests
import json
import time
import os

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-1.5-flash"
NICHE = "D2C brand deals in India"
POSTS_PER_DAY = 5
D2C_BRANDS = ["boAt", "Mamaearth", "Licious", "Bewakoof", "Sugar Cosmetics"]

def generate_blog_post():
    brand = D2C_BRANDS[int(time.time()) % len(D2C_BRANDS)]
    prompt = f"Write a 300-word SEO-optimized blog post on {NICHE} focusing on {brand} offers. Include keywords like '{brand} deals 2025', 'best {brand.lower()} offers'. Structure for Schema.org BlogPosting."
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()
        content = response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        post = {
            "title": f"Top {brand} Deals for {time.strftime('%B %Y')}",
            "content": content,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "post_type": "post",
            "keywords": f"{brand} deals 2025, best {brand.lower()} offers, {brand.lower()} discount"
        }
        with open("posts.json", "a") as f:
            json.dump(post, f)
            f.write("\n")
        print(f"Generated post: {post['title']}")
    except requests.RequestException as e:
        print(f"Error generating post: {e}")

if __name__ == "__main__":
    for _ in range(POSTS_PER_DAY):
        generate_blog_post()
        time.sleep(60)
