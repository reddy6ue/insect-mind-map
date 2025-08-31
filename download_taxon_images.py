import os
import csv
import requests
from bs4 import BeautifulSoup
import time

CSV_FILE = 'referencedata.csv'
IMG_DIR = '.'  # Save images in current directory
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

BING_URL = 'https://www.bing.com/images/search?q={query}+insect+photo&form=HDRSC2'

def sanitize_filename(name):
    return ''.join(c if c.isalnum() else '_' for c in name)

def download_image(taxon):
    query = taxon.replace(' ', '+')
    url = BING_URL.format(query=query)
    print(f"Searching image for {taxon}...")
    resp = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resp.text, 'html.parser')
    images = soup.find_all('a', class_='iusc')
    if not images:
        images = soup.find_all('img')
    img_url = None
    for img in images:
        # Try Bing's data-src or src attributes
        if img.has_attr('m'):  # Bing's metadata
            try:
                import json
                meta = json.loads(img['m'])
                img_url = meta.get('murl')
                if img_url:
                    break
            except Exception:
                continue
        elif img.has_attr('data-src'):
            img_url = img['data-src']
            break
        elif img.has_attr('src'):
            img_url = img['src']
            break
    if img_url:
        ext = os.path.splitext(img_url)[1].split('?')[0]
        fname = sanitize_filename(taxon) + (ext if ext in ['.jpg','.jpeg','.png'] else '.jpg')
        img_path = os.path.join(IMG_DIR, fname)
        try:
            img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded {fname}")
        except Exception as e:
            print(f"Failed to download {img_url}: {e}")
    else:
        print(f"No image found for {taxon}")

def main():
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        taxa = [row['Taxon'] for row in reader]
    for taxon in taxa:
        download_image(taxon)
        time.sleep(2)  # Be polite to Bing

if __name__ == '__main__':
    main()
