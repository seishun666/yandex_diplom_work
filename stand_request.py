from diplom import configuration, data
import requests


def post_new_order(body):
    """Отправляет POST-запрос для создания нового заказа."""
    try:
        response = requests.post(configuration.URL_SERVICE + configuration.CREATE_ORDER_PATH,
                                 json=body,
                                 headers=data.headers)
        response.raise_for_status()  # Поднимает исключение для ошибок 4xx и 5xx
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при создании заказа: {e}")
        return None


def get_order_by_track(track):
    """Получает информацию о заказе по трекеру."""
    get_params = {"t": track}
    try:
        response = requests.get(configuration.URL_SERVICE + configuration.GET_ORDER_PATH,
                                params=get_params)
        response.raise_for_status()  # Поднимает исключение для ошибок
        return response
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении заказа: {e}")
        return None


def create_and_check_order():
    """Создает новый заказ и проверяет его статус."""
    test_order = data.order_body.copy()  # корректное присвоение переменной
    response = post_new_order(test_order)

    if response:
        print("Status code для POST-запроса создания заказа =", response.status_code)

        if response.status_code == 201:
            # Сохранение трека заказа
            resp_dict = response.json()
            track = resp_dict.get("track")
            if track:
                print("Track созданного заказа =", track)

                # Получение информации о заказе по его треку
                get_result = get_order_by_track(track)
                if get_result:
                    print("Status code для GET-запроса информации по заказу с использованием track =",
                          get_result.status_code)
                    if get_result.status_code == 200:
                        print("GET-запрос информации по заказу с использованием track завершился успешно!")
                    else:
                        print("При получении информации о заказе получен неуспешный status code =",
                              get_result.status_code)
            else:
                print("Ответ не содержит track.")
        else:
            print("При создании заказа получен неуспешный status code =", response.status_code)
    else:
        print("Не удалось создать заказ.")


# Вызов функции для создания и проверки заказа
create_and_check_order()