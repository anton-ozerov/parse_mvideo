import json
import os
import time
from datetime import datetime
from math import ceil
import requests as rq
from categories import get_all_categories, get_actual_ids_categories, get_categories_names
from config import items_limit, moscow_cityId, novosibirsk_cityId
from make_requests import get_request


def get_items_of_category(category_id, city_id):
    params = {
        'categoryIds': category_id,
        'offset': '0',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'limit': str(items_limit),
        'doTranslit': 'true',
        'context': 'v2dzaG9wX2lkZFMwMDJsY2F0ZWdvcnlfaWRzn2MxOTX/ZmNhdF9JZGMxOTX/',
    }
    s = rq.Session()
    response = get_request(session=s, url='https://www.mvideo.ru/bff/products/v2/search', params=params,
                           city_id=city_id)
    total_items = response.get('body').get('total')  # Получение кол-ва товаров
    if total_items is None:
        return '[Error] No items'

    pages_count = ceil(total_items / items_limit)
    print(f'[INFO] Total positions: {total_items} | Total pages: {pages_count}')

    products_description = {}
    products_prices = {}

    for page_num in range(pages_count):
        # Ниже получение списка id'шников товаров на страницах
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
            # Объединение информации о товаре и его цены
            for item in products_description.values():
                product_id = item.get('productId')

                if product_id in products_prices:
                    prices = products_prices[product_id]

                    item['item_basePrice'] = prices.get('item_basePrice')
                    item['item_salePrice'] = prices.get('item_salePrice')
                    item['item_bonus'] = prices.get('item_bonus')
                    item['item_link'] = f'https://www.mvideo.ru/products/{item.get("nameTranslit")}-{product_id}'

            print(f'[+] Finished {page_num + 1} of the {pages_count} pages')
    # сохранение в файл данных о товарах данной категории
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
            with (open(f"data\\{'_'.join([novosibirsk_cityId, category_id, 'result.json'])}", encoding="utf-8") as
                  nsk_file):
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
    if not os.path.exists('data'):
        os.mkdir('data')
    if not ('actual_categories.json' in os.listdir('data')):
        with open('data\\actual_categories.json', 'w', encoding='utf-8') as file:
            ph = {"205": "Смартфоны", "118": "Все ноутбуки"}
            json.dump(ph, file, indent=4, ensure_ascii=False)
    get_all_categories()  # вызов функции для получения всех категорий и записи их в файл
    input('Все доступные категории представлены в "data\\all_categories.json".\nА те категории, которые будут сейчас '
          'проанализированы, записаны в "data\\actual_categories.json".\nНа данный момент есть возможность '
          'отредактировать второй файл. После чего, нажмите Enter.')
    all_categories = get_actual_ids_categories()
    print("Выбраны категории:\n" +
          "\n".join([f"{i + 1}. {name}" for i, name in enumerate(get_categories_names(all_categories))]))
    flag = input('\nСобирать статистику для Новосибирска после 20:00 по МСК? (да/нет): ').lower().strip()
    begin = time.time()
    for i, category_id in enumerate(all_categories):
        print(f'[INFO] {category_id} - это {i + 1} из {len(all_categories)}')
        get_items_of_category(category_id, city_id=moscow_cityId)
    print('МОСКВА СДЕЛАНА ЗА', time.time() - begin)
    if flag == 'да':
        now = datetime.now()
        if now.hour < 20:  # сон до 20:00
            time.sleep(round((datetime(now.year, now.month, now.day, 20, 00, 1, 0) -
                              datetime.now()).total_seconds()))

        for i, category_id in enumerate(all_categories):
            get_items_of_category(category_id, city_id=novosibirsk_cityId)
        # input("Продолжаем?: ")  # для тестов
        find_price_up()
        print(time.time() - begin)


if __name__ == '__main__':
    main()
