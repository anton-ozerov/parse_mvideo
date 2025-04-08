import json
from make_requests import get_request


def get_actual_ids_categories() -> list:
    """Читает файл с актуальными категориями из data\\actual_categories.json и возвращает список их id'шников"""
    with open('data\\actual_categories.json', encoding='utf-8') as file:
        popular_categories = json.load(file)
    return list(popular_categories.keys())


def get_all_categories() -> dict:
    """Находит все категории, записывает в файл и возвращает список строк с Id"""
    response = get_request(url='https://www.mvideo.ru/bff/settings/v2/catalog')
    big_categories = response.get('body').get('categories')  # Например: "Техника для кухни", "Аудиотехника"
    categories_ids = {}
    for big_category in big_categories:
        small_categories = big_category.get('categories')  # Например: "Приготовление пищи", "Посуда и аксессуары"
        for small_category in small_categories:
            categories = small_category.get('categories')  # Например: "Мясорубки", "Мультиварки"
            for category in categories:
                url = category.get('url')  # Пример: /melkaya-kuhonnaya-tehnika-3/mikrovolnovye-pechi-94?reff=menu_main
                # Берем 94 (из примера с url)
                category_id = str(url).replace('?', '/').split('/')[-2].split('-')[-1]
                if (('/promo/' not in url and str(url).replace('?', '/').split('/')[-1] == 'reff=menu_main'
                        and len(str(url).replace('?', '/').split('/')) == 4) and
                        category_id not in categories_ids):
                    try:
                        int(category_id)
                        categories_ids[category_id] = category.get('name')
                    except ValueError:  # если не подходящий url
                        pass
    with open('data\\all_categories.json', 'w', encoding="utf-8") as file:
        json.dump(categories_ids, file, indent=4, ensure_ascii=False)
    return categories_ids


def get_categories_names(categories_ids: list) -> list[str]:
    """Получает список id'шников категорий и возвращает список их названий из файла data\\all_categories.json"""
    with open('data\\all_categories.json', encoding='utf-8') as file:
        all_categories = json.load(file)
    return [all_categories[category_id] for category_id in categories_ids]
