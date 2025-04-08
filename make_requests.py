import time
import requests as rq
from config import get_cookies, get_headers, moscow_cityId


def get_request(url: str, params: dict = None, session: rq.Session = None, json_data: dict = None,
                city_id: str = moscow_cityId) -> dict:
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
