import os.path
import time
import requests
from PIL import Image
from io import BytesIO


def get_page(url):
    try:
        cookies = {
            "sessionid": "Suj5xqWg2wNHwwBgle1w6YN5JWm12xpTRTDEvQJIynyKaodbcdHgpXcOqbdLWdEjOmE="
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)

        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")
        return None

def get_text_from_element(element, error_message="Element not found"):
    if element:
        return element.get_text(strip=True)
    print(error_message)
    return None

def get_value_by_key(soup, key_name):
    for item in soup.select(".prod-tec__car"):
        key = item.select_one(".prod-tec__name span")
        value = item.select_one(".prod-tec__value")

        if key and key.text.strip() == key_name:
            return value.text.strip() if value else None

    return None


def upload_catalog_images(image_url):
    SaveDir = os.path.join(os.getcwd(), 'images', 'catalogs')

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)

    if not any(image_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
        return


    response = requests.get(image_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        filename = os.path.join(SaveDir, f'Изображение_{int(time.time())}.webp')
        img.save(filename, 'PNG')
    else:
        print(f"Ошибка загрузки изображения: {response.status_code}")



def upload_product_images(image_url):
    SaveDir = os.path.join(os.getcwd(), 'images', 'products')

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)

    if not any(image_url.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']):
        return


    response = requests.get(image_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        filename = os.path.join(SaveDir, f'Изображение_{int(time.time())}.webp')
        img.save(filename, 'PNG')
    else:
        print(f"Ошибка загрузки изображения: {response.status_code}")