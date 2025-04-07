import json
import os
import time
from datetime import datetime
from math import ceil
import requests as rq
from config import get_cookies, get_headers, items_limit, moscow_cityId, novosibirsk_cityId


def get_request(url: str, params: dict = None, session: rq.Session = None, json_data: dict = None,
                city_id: str = moscow_cityId) -> json:
    """Выполнение request'а и возврат его json'a"""
    time.sleep(1.65)  # При 1.5 не проходит
    status = -1
    response = None
    while status != 200:
        if session is None:
            session = rq  # обычный requests
        if params is None and json_data is None:
            response = session.get(url, cookies=get_cookies(city_id), headers=get_headers())
        elif json_data is None:
            response = session.get(url, cookies=get_cookies(city_id), headers=get_headers(), params=params)
        else:
            response = session.post(url, cookies=get_cookies(city_id), headers=get_headers(), json=json_data)
        status = response.status_code
        if status != 200:
            print('[!] Blocked', time.time())
            time.sleep(5)
            # Не работает, т.к. 5 секунд мало
    return response.json()


def get_categories_ids() -> list[str]:
    """Находит все категории, записывает в файл и возвращает список строк с Id"""
    response = get_request(url='https://www.mvideo.ru/bff/settings/v2/catalog')
    big_categories = response.get('body').get('categories')  # Например: "Техника для кухни", "Аудиотехника"
    with open('all_categories.json', 'w', encoding="utf-8") as file:
        json.dump(big_categories, file, indent=4, ensure_ascii=False)
    categories_ids = set()
    for big_category in big_categories:
        small_categories = big_category.get('categories')  # Например: "Приготовление пищи", "Посуда и аксессуары"
        for small_category in small_categories:
            categories = small_category.get('categories')  # Например: "Мясорубки", "Мультиварки"
            for category in categories:
                url = category.get('url')  # Пример: /melkaya-kuhonnaya-tehnika-3/mikrovolnovye-pechi-94?reff=menu_main
                # Берем 94 (из примера с url)
                category_id = str(url).replace('?', '/').split('/')[-2].split('-')[-1]
                try:
                    int(category_id)
                    categories_ids.add(category_id)
                except ValueError:  # если не подходящий url
                    pass
    return sorted(list(categories_ids))


def get_data(category_id, city_id):
    params = {
        'categoryIds': category_id,
        'offset': '0',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'limit': str(items_limit),
        'doTranslit': 'true',
        'context': 'v2dzaG9wX2lkZFMwMDJsY2F0ZWdvcnlfaWRzn2MxOTX/ZmNhdF9JZGMxOTX/',
    }

    if not os.path.exists('data'):
        os.mkdir('data')

    s = rq.Session()
    response = get_request(session=s, url='https://www.mvideo.ru/bff/products/v2/search', params=params,
                           city_id=city_id)
    total_items = response.get('body').get('total')
    if total_items is None:
        return '[Error] No items'

    pages_count = ceil(total_items / items_limit)
    print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

    products_description = {}
    products_prices = {}

    for page_num in range(pages_count):
        # Ниже получение списка id товаров на страницах
        offset = str(page_num * items_limit)
        params = {
            'categoryIds': category_id,
            'offset': offset,
            'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
            'limit': str(items_limit),
            'doTranslit': 'true',
            'context': 'v2dzaG9wX2lkZFMwMDJsY2F0ZWdvcnlfaWRzn2MxOTX/ZmNhdF9JZGMxOTX/',
        }
        response = get_request(session=s, url='https://www.mvideo.ru/bff/products/v2/search', params=params,
                               city_id=city_id)
        products_ids_list = response.get('body').get('products')
        if products_ids_list:
            # Ниже получение информации о товарах
            json_data = {
                'productIds': products_ids_list,
                'mediaTypes': [
                    'images',
                ],
                'category': True,
                'status': True,
                'brand': True,
                'propertyTypes': [
                    'KEY',
                ],
                'propertiesConfig': {
                    'propertiesPortionSize': 5,
                },
            }
            response = get_request(session=s, url='https://www.mvideo.ru/bff/product-details/list', json_data=json_data,
                                   city_id=city_id)
            for item in response.get('body').get('products'):
                products_description[item.get('productId')] = item
            # Ниже получение цены на товары
            params = {
                'productIds': ','.join(products_ids_list),
                'addBonusRubles': 'true',
                'isPromoApplied': 'true',
            }
            response = get_request(session=s, url='https://www.mvideo.ru/bff/products/prices', params=params,
                                   city_id=city_id)
            material_prices = response.get('body').get('materialPrices')
            for item in material_prices:
                item_id = item.get('price').get('productId')
                item_base_price = item.get('price').get('basePrice')
                item_sale_price = item.get('price').get('salePrice')
                item_bonus = item.get('bonusRubles').get('total')

                products_prices[item_id] = {
                    'item_basePrice': item_base_price,
                    'item_salePrice': item_sale_price,
                    'item_bonus': item_bonus
                }
            # Объединение инфы и цены
            for item in products_description.values():
                product_id = item.get('productId')

                if product_id in products_prices:
                    prices = products_prices[product_id]

                    item['item_basePrice'] = prices.get('item_basePrice')
                    item['item_salePrice'] = prices.get('item_salePrice')
                    item['item_bonus'] = prices.get('item_bonus')
                    item['item_link'] = f'https://www.mvideo.ru/products/{item.get("nameTranslit")}-{product_id}'

            print(f'[+] Finished {page_num + 1} of the {pages_count} pages')
    with open(f'data\\{city_id}_{category_id}_result.json', 'w', encoding="utf-8") as file:
        json.dump(products_description, file, indent=4, ensure_ascii=False)


def find_price_up():
    """Смотрит файлы из /data и сравнивает цены. Различающиеся сохраняет в файл data/RESULT_<секунды>.json"""
    result = []

    listdir = os.listdir('data')  # все файлы из /data
    msk_results = [f"data\\{file_name}" for file_name in listdir if moscow_cityId in file_name]  # только Москва

    for file_name in msk_results:
        category_id = file_name.split('_')[2]

        with open(file_name, encoding="utf-8") as msk_file:  # смотрим файл Москвы
            msk_category = json.load(msk_file)
        if '_'.join([novosibirsk_cityId, category_id, 'result.json']) in listdir:  # Если есть, смотрим файл Новосибирск
            print(f"data\\{'_'.join([novosibirsk_cityId, category_id, 'result.json'])}")
            with open(f"data\\{'_'.join([novosibirsk_cityId, category_id, 'result.json'])}", encoding="utf-8") as nsk_file:
                nsk_category = json.load(nsk_file)

            for msk_item in msk_category.values():
                msk_id = msk_item.get('productId')
                msk_saleprice = msk_item.get('item_salePrice')

                if msk_id in nsk_category.keys():
                    nsk_saleprice = nsk_category[msk_id].get('item_salePrice')
                    if msk_saleprice < nsk_saleprice:
                        copy = nsk_category[msk_id].copy()
                        copy['old_price'] = msk_saleprice
                        result.append(copy)
    with open(f'data\\RESULT_{time.time()}.json', 'w', encoding="utf-8") as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def main():
    flag = input('Собирать статистику для Новосибирска после 20:00 по МСК? (да/нет): ').lower().strip()
    all_begin = time.time()
    all_categories = get_categories_ids()
    # all_categories = get_categories_ids()[:2]  # для тестов
    begin = time.time()
    for i, category_id in enumerate(all_categories):
        print(f'[INFO] {category_id} - это {i + 1} из {len(all_categories)}')
        get_data(category_id, city_id=moscow_cityId)
    print('МОСКВА СДЕЛАНА ЗА', time.time() - begin)
    if flag == 'да':
        now = datetime.now()
        if now.hour < 20:  # сон до 20:00
            time.sleep(round((datetime(now.year, now.month, now.day, 20, 00, 1, 0) -
                              datetime.now()).total_seconds()))

        for i, category_id in enumerate(all_categories):
            get_data(category_id, city_id=novosibirsk_cityId)
        # input("Продолжаем?: ")  # для тестов
        find_price_up()
        print(time.time() - all_begin)


if __name__ == '__main__':
    main()
