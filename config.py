from fake_useragent import UserAgent


items_limit = 48
moscow_cityId = 'CityCZ_975'
novosibirsk_cityId = 'CityCZ_2246'


def get_cookies(city_id: str = moscow_cityId) -> dict:
    """Передается нужный cityId. От этого изменяется timezone. Варианты: только
    moscow_cityId или novosibirsk_cityId. Если другое, то изменяется на Москву. Возвращает словарь с cookies."""
    if city_id not in (moscow_cityId, novosibirsk_cityId):
        city_id = moscow_cityId

    if city_id == moscow_cityId:
        cookies = {
            'edit': 'edit',
            'MVID_CITY_ID': 'CityCZ_975',
            'MVID_REGION_ID': '1',
            'MVID_TIMEZONE_OFFSET': '3',
            'MVID_REGION_SHOP': 'S002',
        }
    else:  # только city_id == novosibirsk_cityId
        cookies = {
            'edit': 'edit',
            'MVID_CITY_ID': 'CityCZ_2246',
            'MVID_REGION_ID': '29',
            'MVID_TIMEZONE_OFFSET': '7',
            'MVID_KLADR_ID': '5400000100000',
            'MVID_REGION_SHOP': 'S955',
        }
    return cookies


def get_headers() -> dict:
    """Возвращает словарь с headers с fake'овым user-agent"""
    headers = {
        'edit': 'edit',
    }
    return headers
