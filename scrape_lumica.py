
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import urljoin, urlparse

URL = "https://lumicawebdesign.com/blog/"
HEADERS = {
    "User-Agent": "founders25-scraper/1.0 (+https://github.com/JoseMas68/founders25-scraper)"
}
RATE_LIMIT_SECONDS = 3
IMAGES_DIR = "lumica_images"

def download_image(img_url, post_title):
    if not img_url:
        return None
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    try:
        img_name = post_title.replace(" ", "_")[:40]  # nombre corto y seguro
        ext = os.path.splitext(urlparse(img_url).path)[1] or ".jpg"
        local_path = os.path.join(IMAGES_DIR, f"{img_name}{ext}")
        r = requests.get(img_url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(r.content)
        return local_path
    except Exception as e:
        print(f"Error descargando imagen: {img_url} - {e}")
        return None

def scrape_blog(url):
    print(f"Scrapeando: {url}")
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    posts = []
    for article in soup.select("article"):
        title_tag = article.select_one("h2 a, h1 a")
        if title_tag:
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            # Buscar imagen principal del post
            img_tag = article.select_one("img")
            img_url = None
            if img_tag and img_tag.get("src"):
                img_url = urljoin(url, img_tag.get("src"))
                img_local = download_image(img_url, title)
            else:
                img_local = None
            posts.append({"title": title, "url": link, "image_url": img_url, "image_local": img_local})

    print(f"Encontrados {len(posts)} posts.")
    return posts

def main():
    posts = scrape_blog(URL)
    df = pd.DataFrame(posts)
    df.to_csv("lumica_blog_posts.csv", index=False, encoding="utf-8")
    print("Datos guardados en lumica_blog_posts.csv y las imágenes en lumica_images/")
    time.sleep(RATE_LIMIT_SECONDS)

if __name__ == "__main__":
    main()
