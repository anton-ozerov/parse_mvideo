import requests as rq
import json


def get_data():
    cookies = {
        '__lhash_': 'eaa407f5284800d2a2df12501042245d',
        'MVID_REGION_ID': '1',
        'MVID_CITY_ID': 'CityCZ_975',
        'MVID_TIMEZONE_OFFSET': '3',
        'MVID_KLADR_ID': '7700000000000',
        'MVID_REGION_SHOP': 'S002',
        'MVID_NEW_LK_OTP_TIMER': 'true',
        'MVID_CHAT_VERSION': '6.6.0',
        'SENTRY_TRANSACTIONS_RATE': '0.1',
        'SENTRY_REPLAYS_SESSIONS_RATE': '0.01',
        'SENTRY_REPLAYS_ERRORS_RATE': '0.01',
        'SENTRY_ERRORS_RATE': '0.1',
        'MVID_FILTER_CODES': 'true',
        'MVID_SUGGEST_DIGINETICA': 'true',
        'MVID_MEDIA_STORIES': 'true',
        'MVID_SERVICES': '111',
        'MVID_FLOCKTORY_ON': 'true',
        'MVID_IS_NEW_BR_WIDGET': 'true',
        'MVID_NEW_LK_CHECK_CAPTCHA': 'true',
        'MVID_GTM_ENABLED': '011',
        'MVID_CRITICAL_GTM_INIT_DELAY': '3000',
        'MVID_WEB_SBP': 'true',
        'MVID_CREDIT_SERVICES': 'true',
        'MVID_TYP_CHAT': 'true',
        'MVID_SP': 'true',
        'MVID_CREDIT_DIGITAL': 'true',
        'MVID_CASCADE_CMN': 'true',
        'MVID_EMPLOYEE_DISCOUNT': 'true',
        'MVID_AB_UPSALE': 'true',
        'MVID_AB_PERSONAL_RECOMMENDS': 'true',
        'MVID_SERVICE_AVLB': 'true',
        'MVID_NEW_CHAT_PDP': 'true',
        'MVID_TYP_ACCESSORIES_ORDER_SET': 'true',
        'MVID_GROUP_BY_QUALITY': 'true',
        'MVID_DISPLAY_PERS_DISCOUNT': 'true',
        'MVID_AB_PERSONAL_RECOMMENDS_SRP': 'true',
        'MVID_DIGINETICA_ENABLED': 'true',
        'MVID_ACCESSORIES_ORDER_SET_VERSION': '2',
        'MVID_BYPASS_FC': 'true',
        'MVID_IMG_RESIZE': 'true',
        'MVID_NEW_GET_SHOPPING_CART_SHORT': 'true',
        'MVID_WEB_QR': 'true',
        'MVID_SRP_DIGINETICA_ENABLED': 'true',
        'MVID_ALLPROMOTIONS_NEW': 'true',
        'MVID_SORM_INTEGRATION': 'true',
        'MVID_QUASAR_CUSTOMER': 'true',
        'MVID_QUASAR_CAPTCHA': 'true',
        'MVID_QUASAR_UPDATE_CUSTOMER': 'true',
        'MVID_ACTIVATE_BONUSES_MCOMBO': 'true',
        'MVID_DISABLEDITEM_PRICE': '1',
        'MVID_RECOMENDATION_SET_ALGORITHM': '2',
        'MVID_ENVCLOUD': 'prod1',
        'MVID_DEVICE_UUID': '038d325e-31fa-4ee8-bc25-c2c2e4df7eb9',
        '_userGUID': '0:m92h6ghz:xOyvQrIPs4Boz1MjA~1kvJMXRkBxQs6v',
        'mindboxDeviceUUID': '01f1fda1-4158-4b95-a377-7dc10d679fca',
        'directCrm-session': '%7B%22deviceGuid%22%3A%2201f1fda1-4158-4b95-a377-7dc10d679fca%22%7D',
        '_userGUID': '0:m92h6ghz:xOyvQrIPs4Boz1MjA~1kvJMXRkBxQs6v',
        '_ym_uid': '1743752440670314607',
        '_ym_d': '1743752440',
        '_ga': 'GA1.1.1722396845.1743752443',
        '_ym_isad': '1',
        'flocktory-uuid': 'c5178c35-c257-4604-9521-66f562b91118-5',
        'advcake_track_id': 'b17c03ee-ad22-07e4-8002-51a880913c10',
        'advcake_session_id': 'fddb2f33-1028-0a52-00d9-cf616e8e98ef',
        'uxs_uid': '1d816a30-1128-11f0-9afa-abbefa25b897',
        'flacktory': 'no',
        'BIGipServeratg-ps-prod_tcp80': '2466569226.20480.0000',
        'bIPs': '-314595793',
        'adid': '174375244489014',
        'afUserId': 'f10f82a9-ac69-4f0d-8aa1-1194db8df633-p',
        'MVID_GEOLOCATION_NEEDED': 'false',
        'digi_uc': '|c:174375:400321432',
        'advcake_track_url': '%3D202501134YQaG5fwuSLN92teUE62eQPJ04y770zzmQTjxfR02%2BY0zYWMVRpWBenKegGfdNbZXC7UqPPE28Wzz2rRE6iud1JI4PN0yz%2B2x9jyQpST3P0mO178iMhzQ%2FKWcsrpfwZ%2BT7hRnTBISD2gQJUGRwLt1Z5xgBYtp%2BmZ2uVCfnXVX3WGsvb%2BmYO0hoojSwxNxI4Azo5hhS1K%2Fy6P4uR%2BwXOdmuJifUGZ1DKTqKxWNFs5piDCUP%2BOybcCTDnQUi5myaUjcThMp%2Bn1AnUvcI3u9iqVuC9CTt5XQxDCzvRpIspa4inirnQKZnBSkcFjYtpg6G3mz54y1UjBrK6JEtIZAbmJPARkCy3j4w2HLRTnluKc6lMMtCvfNs9NzkSHi3bhEcpm3ujJV8k4QJoxedZBzr3sf%2FYKsHWNyGqwIa2k6XCjovgnVqFEPYqLo8Z7XRD2FbWwi3lusardzoTMJA5Il1Z72z1tUtNqTGBAhf9tHN9egXIGDMSBoLF1SESUYKwZCxN%2FImhoz5%2FYC4iEU9nydlmbBjt%2FCAWBwi7oxmr%2FHy34ohtEJWvL7FEInf7RWYmXSM1IVC7JXoqZBg49vmOTWDj7SbjAP0VGvlbUb9JQMa7xYKettpw%2BCdduH0nrW2xuwYIlwgd85yhDgU88O7whaYwmQAgxo1thoaMwUKxxADZ4aYYgZlquj9yulto%3D',
        '_sp_id.d61c': '19444a8f-2694-4dff-be95-436787153f3d.1743752441.1.1743754012..3a61907f-8cd3-4b1c-86ef-44192f0e610a..cbcb5c4f-e61b-4e9c-bdcc-82858396b608.1743752440507.166',
        '__hash_': '60bde8a61bb5856fe78d1b9f9d8d7bdd',
        'gsscgib-w-mvideo': 'P8T4Sr0FsQuAJYpyI57qJRrJ02TDIfQ0mE9zxB8PvnEu2E2DPiAPKhzeeEF48ECdtD0WURcFXngbGTUYDauhOLuSpoWZ+GymVbPHbZwVmALQ+heW0awEnCaYw77hy4e1qO1dnFu1vMkiZ5g8LVX8cP78nSRuns793mMnMzSFtEk4IRjX7fc9uRPR66D46TKwh+/Acva+wGouHwetyvszv9mwV2WJ3nev0ZmTA4SmFAEHrIkkTqmz8PV2HymD5kCwPrCzO08fqbPy3QWISFbfGlfYz0GBIg==',
        'gsscgib-w-mvideo': 'P8T4Sr0FsQuAJYpyI57qJRrJ02TDIfQ0mE9zxB8PvnEu2E2DPiAPKhzeeEF48ECdtD0WURcFXngbGTUYDauhOLuSpoWZ+GymVbPHbZwVmALQ+heW0awEnCaYw77hy4e1qO1dnFu1vMkiZ5g8LVX8cP78nSRuns793mMnMzSFtEk4IRjX7fc9uRPR66D46TKwh+/Acva+wGouHwetyvszv9mwV2WJ3nev0ZmTA4SmFAEHrIkkTqmz8PV2HymD5kCwPrCzO08fqbPy3QWISFbfGlfYz0GBIg==',
        'fgsscgib-w-mvideo': 'kBXJ2fd98819751d4ad29956afc36f31782809f7',
        'fgsscgib-w-mvideo': 'kBXJ2fd98819751d4ad29956afc36f31782809f7',
        'gsscgib-w-mvideo': 'zf3YhsETZEfYsM4LERRtnpGg6oQHZUptP2o3h8Joet2Y7DTJjuPQbvNh0C3icA3jcy1U4m32CFGGZpIdudnjLRFE35yS9Q2xQer6w8n5yH7QaW5+hVBfXOElvr0dFNnYfU05Y7ubX1XOkzcbUtJDqhwpM3FzbLwi2fQRFL6W9UrhI35ooL7/0i3ZtwaW0NueyQ2YumAU7rt9LPYUw/PxC9hHPfbHFAqg6yzIoEKAUspSBjXnRVRidV6b8ItWa7VhwTdKnRQbH5q5I3QyjdM+dWRYNaeZpA==',
        'cfidsgib-w-mvideo': 'T2sRsZvJJy72NdKQMF1tqkZxemfJK31aHS+9X5+X9KN4GPvGKiZ7PD5ZXeFOt3HiM5+5mNl1fBGRea6xJIRvtDVLfGHukcEGxtk1ue/uABtllZ9Ddrfq6TYUFq65Ay79rJsKfnunpzQ7VdeaR5BO8wR0CUHVRa4AF69B1l0=',
        '_ga_CFMZTSS5FM': 'GS1.1.1743755853.2.0.1743755853.0.0.0',
        '_ga_BNX5WPP3YK': 'GS1.1.1743755853.2.0.1743755853.60.0.0',
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'baggage': 'sentry-environment=production,sentry-release=release_25_3_4(11296),sentry-public_key=ae7d267743424249bfeeaa2e347f4260,sentry-trace_id=bf0c15bf3631424db33f1702a4f91c90,sentry-transaction=%2F**%2F,sentry-sampled=false,sentry-sample_rand=0.8347345062618879,sentry-sample_rate=0.1',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.mvideo.ru/noutbuki-planshety-komputery-8/planshety-195',
        'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sentry-trace': 'bf0c15bf3631424db33f1702a4f91c90-b288c2e14c98f293-0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
        'x-set-application-id': '4c67ffa1-421f-4a65-88d1-63a295468fa0',
        # 'cookie': '__lhash_=eaa407f5284800d2a2df12501042245d; MVID_REGION_ID=1; MVID_CITY_ID=CityCZ_975; MVID_TIMEZONE_OFFSET=3; MVID_KLADR_ID=7700000000000; MVID_REGION_SHOP=S002; MVID_NEW_LK_OTP_TIMER=true; MVID_CHAT_VERSION=6.6.0; SENTRY_TRANSACTIONS_RATE=0.1; SENTRY_REPLAYS_SESSIONS_RATE=0.01; SENTRY_REPLAYS_ERRORS_RATE=0.01; SENTRY_ERRORS_RATE=0.1; MVID_FILTER_CODES=true; MVID_SUGGEST_DIGINETICA=true; MVID_MEDIA_STORIES=true; MVID_SERVICES=111; MVID_FLOCKTORY_ON=true; MVID_IS_NEW_BR_WIDGET=true; MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_GTM_ENABLED=011; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_WEB_SBP=true; MVID_CREDIT_SERVICES=true; MVID_TYP_CHAT=true; MVID_SP=true; MVID_CREDIT_DIGITAL=true; MVID_CASCADE_CMN=true; MVID_EMPLOYEE_DISCOUNT=true; MVID_AB_UPSALE=true; MVID_AB_PERSONAL_RECOMMENDS=true; MVID_SERVICE_AVLB=true; MVID_NEW_CHAT_PDP=true; MVID_TYP_ACCESSORIES_ORDER_SET=true; MVID_GROUP_BY_QUALITY=true; MVID_DISPLAY_PERS_DISCOUNT=true; MVID_AB_PERSONAL_RECOMMENDS_SRP=true; MVID_DIGINETICA_ENABLED=true; MVID_ACCESSORIES_ORDER_SET_VERSION=2; MVID_BYPASS_FC=true; MVID_IMG_RESIZE=true; MVID_NEW_GET_SHOPPING_CART_SHORT=true; MVID_WEB_QR=true; MVID_SRP_DIGINETICA_ENABLED=true; MVID_ALLPROMOTIONS_NEW=true; MVID_SORM_INTEGRATION=true; MVID_QUASAR_CUSTOMER=true; MVID_QUASAR_CAPTCHA=true; MVID_QUASAR_UPDATE_CUSTOMER=true; MVID_ACTIVATE_BONUSES_MCOMBO=true; MVID_DISABLEDITEM_PRICE=1; MVID_RECOMENDATION_SET_ALGORITHM=2; MVID_ENVCLOUD=prod1; MVID_DEVICE_UUID=038d325e-31fa-4ee8-bc25-c2c2e4df7eb9; _userGUID=0:m92h6ghz:xOyvQrIPs4Boz1MjA~1kvJMXRkBxQs6v; mindboxDeviceUUID=01f1fda1-4158-4b95-a377-7dc10d679fca; directCrm-session=%7B%22deviceGuid%22%3A%2201f1fda1-4158-4b95-a377-7dc10d679fca%22%7D; _userGUID=0:m92h6ghz:xOyvQrIPs4Boz1MjA~1kvJMXRkBxQs6v; _ym_uid=1743752440670314607; _ym_d=1743752440; _ga=GA1.1.1722396845.1743752443; _ym_isad=1; flocktory-uuid=c5178c35-c257-4604-9521-66f562b91118-5; advcake_track_id=b17c03ee-ad22-07e4-8002-51a880913c10; advcake_session_id=fddb2f33-1028-0a52-00d9-cf616e8e98ef; uxs_uid=1d816a30-1128-11f0-9afa-abbefa25b897; flacktory=no; BIGipServeratg-ps-prod_tcp80=2466569226.20480.0000; bIPs=-314595793; adid=174375244489014; afUserId=f10f82a9-ac69-4f0d-8aa1-1194db8df633-p; MVID_GEOLOCATION_NEEDED=false; digi_uc=|c:174375:400321432; advcake_track_url=%3D202501134YQaG5fwuSLN92teUE62eQPJ04y770zzmQTjxfR02%2BY0zYWMVRpWBenKegGfdNbZXC7UqPPE28Wzz2rRE6iud1JI4PN0yz%2B2x9jyQpST3P0mO178iMhzQ%2FKWcsrpfwZ%2BT7hRnTBISD2gQJUGRwLt1Z5xgBYtp%2BmZ2uVCfnXVX3WGsvb%2BmYO0hoojSwxNxI4Azo5hhS1K%2Fy6P4uR%2BwXOdmuJifUGZ1DKTqKxWNFs5piDCUP%2BOybcCTDnQUi5myaUjcThMp%2Bn1AnUvcI3u9iqVuC9CTt5XQxDCzvRpIspa4inirnQKZnBSkcFjYtpg6G3mz54y1UjBrK6JEtIZAbmJPARkCy3j4w2HLRTnluKc6lMMtCvfNs9NzkSHi3bhEcpm3ujJV8k4QJoxedZBzr3sf%2FYKsHWNyGqwIa2k6XCjovgnVqFEPYqLo8Z7XRD2FbWwi3lusardzoTMJA5Il1Z72z1tUtNqTGBAhf9tHN9egXIGDMSBoLF1SESUYKwZCxN%2FImhoz5%2FYC4iEU9nydlmbBjt%2FCAWBwi7oxmr%2FHy34ohtEJWvL7FEInf7RWYmXSM1IVC7JXoqZBg49vmOTWDj7SbjAP0VGvlbUb9JQMa7xYKettpw%2BCdduH0nrW2xuwYIlwgd85yhDgU88O7whaYwmQAgxo1thoaMwUKxxADZ4aYYgZlquj9yulto%3D; _sp_id.d61c=19444a8f-2694-4dff-be95-436787153f3d.1743752441.1.1743754012..3a61907f-8cd3-4b1c-86ef-44192f0e610a..cbcb5c4f-e61b-4e9c-bdcc-82858396b608.1743752440507.166; __hash_=60bde8a61bb5856fe78d1b9f9d8d7bdd; gsscgib-w-mvideo=P8T4Sr0FsQuAJYpyI57qJRrJ02TDIfQ0mE9zxB8PvnEu2E2DPiAPKhzeeEF48ECdtD0WURcFXngbGTUYDauhOLuSpoWZ+GymVbPHbZwVmALQ+heW0awEnCaYw77hy4e1qO1dnFu1vMkiZ5g8LVX8cP78nSRuns793mMnMzSFtEk4IRjX7fc9uRPR66D46TKwh+/Acva+wGouHwetyvszv9mwV2WJ3nev0ZmTA4SmFAEHrIkkTqmz8PV2HymD5kCwPrCzO08fqbPy3QWISFbfGlfYz0GBIg==; gsscgib-w-mvideo=P8T4Sr0FsQuAJYpyI57qJRrJ02TDIfQ0mE9zxB8PvnEu2E2DPiAPKhzeeEF48ECdtD0WURcFXngbGTUYDauhOLuSpoWZ+GymVbPHbZwVmALQ+heW0awEnCaYw77hy4e1qO1dnFu1vMkiZ5g8LVX8cP78nSRuns793mMnMzSFtEk4IRjX7fc9uRPR66D46TKwh+/Acva+wGouHwetyvszv9mwV2WJ3nev0ZmTA4SmFAEHrIkkTqmz8PV2HymD5kCwPrCzO08fqbPy3QWISFbfGlfYz0GBIg==; fgsscgib-w-mvideo=kBXJ2fd98819751d4ad29956afc36f31782809f7; fgsscgib-w-mvideo=kBXJ2fd98819751d4ad29956afc36f31782809f7; gsscgib-w-mvideo=zf3YhsETZEfYsM4LERRtnpGg6oQHZUptP2o3h8Joet2Y7DTJjuPQbvNh0C3icA3jcy1U4m32CFGGZpIdudnjLRFE35yS9Q2xQer6w8n5yH7QaW5+hVBfXOElvr0dFNnYfU05Y7ubX1XOkzcbUtJDqhwpM3FzbLwi2fQRFL6W9UrhI35ooL7/0i3ZtwaW0NueyQ2YumAU7rt9LPYUw/PxC9hHPfbHFAqg6yzIoEKAUspSBjXnRVRidV6b8ItWa7VhwTdKnRQbH5q5I3QyjdM+dWRYNaeZpA==; cfidsgib-w-mvideo=T2sRsZvJJy72NdKQMF1tqkZxemfJK31aHS+9X5+X9KN4GPvGKiZ7PD5ZXeFOt3HiM5+5mNl1fBGRea6xJIRvtDVLfGHukcEGxtk1ue/uABtllZ9Ddrfq6TYUFq65Ay79rJsKfnunpzQ7VdeaR5BO8wR0CUHVRa4AF69B1l0=; _ga_CFMZTSS5FM=GS1.1.1743755853.2.0.1743755853.0.0.0; _ga_BNX5WPP3YK=GS1.1.1743755853.2.0.1743755853.60.0.0',
    }

    params = {
        'categoryIds': '195',
        'offset': '0',
        'filterParams': 'WyJ0b2xrby12LW5hbGljaGlpIiwiLTEyIiwiZGEiXQ==',
        'limit': '48',
        'doTranslit': 'true',
        'context': 'v2dzaG9wX2lkZFMwMDJsY2F0ZWdvcnlfaWRzn2MxOTX/ZmNhdF9JZGMxOTX/',
    }

    response = rq.get('https://www.mvideo.ru/bff/products/v2/search', params=params, cookies=cookies,
                      headers=headers).json()
    # print(response)

    products_ids = response.get('body').get('products')

    with open('1_products_ids.json', 'w') as file:
        json.dump(products_ids, file, indent=4, ensure_ascii=False)

    # print(products_ids)

    json_data = {
        'productIds': products_ids,
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

    response = rq.post('https://www.mvideo.ru/bff/product-details/list', cookies=cookies, headers=headers,
                             json=json_data).json()
    with open('2_items.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    # print(len(response.get('body').get('products')))

    products_ids_str = ','.join(products_ids)

    params = {
        'productIds': products_ids_str,
        'addBonusRubles': 'true',
        'isPromoApplied': 'true',
    }

    response = rq.get('https://www.mvideo.ru/bff/products/prices', params=params, cookies=cookies,
                            headers=headers).json()

    with open('3_prices.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    items_prices = {}

    material_prices = response.get('body').get('materialPrices')

    for item in material_prices:
        item_id = item.get('price').get('productId')
        item_base_price = item.get('price').get('basePrice')
        item_sale_price = item.get('price').get('salePrice')
        item_bonus = item.get('bonusRubles').get('total')

        items_prices[item_id] = {
            'item_basePrice': item_base_price,
            'item_salePrice': item_sale_price,
            'item_bonus': item_bonus
        }

    with open('4_items_prices.json', 'w') as file:
        json.dump(items_prices, file, indent=4, ensure_ascii=False)


def get_result():
    with open('2_items.json') as file:
        products_data = json.load(file)

    with open('4_items_prices.json') as file:
        products_prices = json.load(file)

    products_data = products_data.get('body').get('products')

    for item in products_data:
        product_id = item.get('productId')

        if product_id in products_prices:
            prices = products_prices[product_id]

            item['item_basePrice'] = prices.get('item_basePrice')
            item['item_salePrice'] = prices.get('item_salePrice')
            item['item_bonus'] = prices.get('item_bonus')

    with open('5_result.json', 'w') as file:
        json.dump(products_data, file, indent=4, ensure_ascii=False)


def main():
    get_data()
    get_result()


if __name__ == '__main__':
    main()
