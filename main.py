import pandas as pd
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import utils

CatalogUrl = 'https://www.vamsvet.ru/catalog/section/elektrotovary/#p{}'

# здесь оставил для того чтобы могли вручную указать страницу,
# Можно заменить на любую категорию, например 'elektrotovary'





BaseUrl = 'https://www.vamsvet.ru/'

data = []

# Максимальная кол-во товаров
MAX_PRODUCTS = 1

def save_to_excel():
    """Сохранение данных в Excel"""
    df = pd.DataFrame(data).drop_duplicates(subset=["Номер товара"])
    df = df.head(MAX_PRODUCTS)
    df.to_excel('product.xlsx', index=False)
    print('Данные сохранены в products.xlsx, изображения в /images')

def get_product_description(driver, product_url, product_id):
    if len(data) >= MAX_PRODUCTS:
        print("Достигнут предел добавленных товаров.")
        save_to_excel()
        return

    driver.get(product_url)
    # time.sleep(2)

    # if any(item["Номер товара"] == product_id for item in data):
    #     print(f"Товар с ID {product_id} уже добавлен, пропускаем.")
    #     return

    # print(f"Парсим товар: {product_url}")

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    title = soup.find('h1', class_='page-title _var-2')
    price = soup.find('div', class_='buy-info__p-new opt-price')
    clean_price = price.text.replace(" ", "").replace("₽", "").strip() if price else None

    description = soup.find('div', class_='pr-page__text')
    breadcrumb_items = soup.find_all('a', class_='breadcrumbs__link')

    category_name = breadcrumb_items[2].text.strip() if len(breadcrumb_items) > 2 else None
    subcategory_name = breadcrumb_items[3].text.strip() if len(breadcrumb_items) > 3 else None

    articul = soup.find("div", class_="prod-tec__value")
    brand = utils.get_value_by_key(soup, "Бренд")
    region_brand = utils.get_value_by_key(soup, "Страна бренда")
    region_manufacture = utils.get_value_by_key(soup, "Страна производства")
    collection_by = utils.get_value_by_key(soup, "Коллекция")
    style = utils.get_value_by_key(soup, "Стиль")

    # Размеры
    height = utils.get_value_by_key(soup, "Высота, мм")
    diameter = utils.get_value_by_key(soup, "Диаметр, мм")
    weight = utils.get_value_by_key(soup, "Вес, кг")

    # Лампы
    plinth_type = utils.get_value_by_key(soup, "Тип цоколя")
    type_bulb_main = utils.get_value_by_key(soup, "Тип лампочки (основной)")
    count_lamps = utils.get_value_by_key(soup, "Количество ламп")
    lamp_power = utils.get_value_by_key(soup, "Мощность лампы, W")
    general_power = utils.get_value_by_key(soup, "Общая мощность, W")
    lighting_area = utils.get_value_by_key(soup, "Площадь освещения, м2")
    voltage = utils.get_value_by_key(soup, "Напряжение, V")

    # Цвет и материал
    material_type = utils.get_value_by_key(soup, "Виды материалов")
    armature_material = utils.get_value_by_key(soup, "Материал арматуры")
    material_plafonds = utils.get_value_by_key(soup, "Материал плафонов")
    direction_plafonds = utils.get_value_by_key(soup, "Направление плафонов")
    type_diffuser = utils.get_value_by_key(soup, "Вид рассеивателя")
    diffuser_shape = utils.get_value_by_key(soup, "Форма рассеивателя")
    color = utils.get_value_by_key(soup, "Цвет")
    armature_color = utils.get_value_by_key(soup, "Цвет арматуры")
    plafonds_color = utils.get_value_by_key(soup, "Цвет плафонов")

    # Дополнительно
    degree_protection = utils.get_value_by_key(soup, "Степень защиты")
    interior = utils.get_value_by_key(soup, "Интерьер")
    place_installation = utils.get_value_by_key(soup, "Место установки")
    mounting_type = utils.get_value_by_key(soup, "Тип крепления")
    for_stretch_ceilings = utils.get_value_by_key(soup, "Подходит для натяжных потолков")
    for_low_ceilings = utils.get_value_by_key(soup, "Подходит для низких потолков")
    manufacturers_warranty = utils.get_value_by_key(soup, "Гарантия производителя")
    store_warranty = utils.get_value_by_key(soup, "Гарантия магазина")
    service_life = utils.get_value_by_key(soup, "Срок службы")


    images_list = []
    images = soup.find_all("a", class_="product-pic__tumb")

    for img in images:
        img_url = img.get("href")
        if img_url:
            full_url = urljoin(BaseUrl, img_url)
            images_list.append(full_url)

    for img_url in images_list:
        utils.upload_product_images(img_url)

    data.append({
        # Основные характеристики
        "Номер товара": product_id,
        "Название": title.text.strip() if title else None,
        "Цена": clean_price if clean_price else None,
        "Категория": f"{category_name} > {subcategory_name}",
        "Описание": description.text.strip() if description else None,
        "Артикул": articul.text.strip() if articul else None,
        "Бренд": brand,
        "Страна бренда": region_brand,
        "Страна производства": region_manufacture,
        "Коллекция": collection_by,
        "Стиль": style,

        # Размеры
        "Высота, мм": height if height else None,
        "Диаметр, мм": diameter if diameter else None,
        "Вес, кг": weight if weight else None,

        # Лампы
        "Тип цоколя": plinth_type if plinth_type else None,
        "Тип лампочки (основной)": type_bulb_main if type_bulb_main else None,
        "Количество ламп": count_lamps if count_lamps else None,
        "Мощность лампы, W": lamp_power if lamp_power else None,
        "Общая мощность, W": general_power if general_power else None,
        "Площадь освещения, м2": lighting_area if lighting_area else None,
        "Напряжение, V": voltage if voltage else None,

        # Цвет и материал
        "Вид материала": material_type if material_type else None,
        "Материал арматуры": armature_material if armature_material else None,
        "Материал плафонов": material_plafonds if material_plafonds else None,
        "Направление плафонов": direction_plafonds if direction_plafonds else None,
        "Вид рассеивателя": type_diffuser if type_diffuser else None,
        "Форма рассеивателя": diffuser_shape if diffuser_shape else None,
        "Цвет": color if color else None,
        "Цвет арматуры": armature_color if armature_color else None,
        "Цвет плафонов": plafonds_color if plafonds_color else None,

        # Дополнительно
        "Степень защиты": degree_protection if degree_protection else None,
        "Интерьер": interior if interior else None,
        "Место установки": place_installation if place_installation else None,
        "Тип крепления": mounting_type if mounting_type else None,
        "Подходит для натяжных потолков": for_stretch_ceilings if for_stretch_ceilings else None,
        "Подходит для низких потолков": for_low_ceilings if for_low_ceilings else None,
        "Гарантия производителя": manufacturers_warranty if manufacturers_warranty else None,
        "Гарантия магазина": store_warranty if store_warranty else None,
        "Срок службы": service_life if service_life else None,
    })
    if len(data) >= MAX_PRODUCTS:
        save_to_excel()


def get_product_ids_from_catalog(driver, catalog_url):
    driver.get(catalog_url)
    # time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    product_links = soup.find_all('a', class_='js-cd-link')
    # category_link_tag = soup.find('a', class_='s-menu__item')['href']

    products = set()

    for product_link in product_links:
        product_url = urljoin(BaseUrl, product_link['href'])
        product_id = product_link.get('data-id')
        if product_id and product_id not in products:
            products.add((product_url, product_id))

    return list(products)


def get_catalog():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920x1080")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    page = 1

    while True:
        catalog_url = CatalogUrl.format(page)
        print(f"Загружаем страницу каталога: {catalog_url}")

        product_list = get_product_ids_from_catalog(driver, catalog_url)

        if not product_list:
            print("Больше страниц нет, заканчиваем.")
            break

        for product_url, product_id in product_list:
            get_product_description(driver, product_url, product_id)
            if len(data) >= MAX_PRODUCTS:
                save_to_excel()
                driver.quit()
                return

        page += 1

    driver.quit()

get_catalog()
