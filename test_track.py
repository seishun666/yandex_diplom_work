from diplom import data, stand_request


def create_and_check_order():
    """Создает новый заказ и проверяет его статус."""
    test_order = data.order_body.copy()  # корректное присвоение переменной
    response = stand_request.post_new_order(test_order)

    if response:
        print("Status code для POST-запроса создания заказа =", response.status_code)

        if response.status_code == 201:
            # Сохранение трека заказа
            resp_dict = response.json()
            track = resp_dict.get("track")
            if track:
                print("Track созданного заказа =", track)

                # Получение информации о заказе по его треку
                get_result = stand_request.get_order_by_track(track)
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


def test_post_new_order():
    test_order = data.order_body.copy()
    response = stand_request.post_new_order(test_order)
    assert response.status_code == 201  # Проверка, что статус код 201


def test_get_order_by_track():
    test_order = data.order_body.copy()
    response = stand_request.post_new_order(test_order)
    assert response.status_code == 201
    if response.status_code == 201:
        track = response.json().get("track")
        get_result = stand_request.get_order_by_track(track)
        assert get_result.status_code == 200  # Проверка, что статус код 200
