import sender_stand_request
import data


def get_user_body(first_name):  # эта функция меняет значения в параметре firstName
    current_body = data.user_body.copy() # копирование словаря с телом запроса из файла data, чтобы не потерять данные в исходном словаре
    current_body["firstName"] = first_name  # изменение значения в поле firstName
    return current_body  # возвращается новый словарь с нужным значением firstName

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

# def test_create_user_2_letter_in_first_name_get_success_response():
#     user_body = get_user_body("Аа")  # В переменную user_body сохраняется обновленное тело запроса с именем “Аа”
#     user_response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя
#     assert user_response.status_code == 201  # Проверяется, что код ответа равен 201
#     assert user_response.json()["authToken"] != ""  # Проверяется, что в ответе есть поле authToken, и оно не пустое
#
#     users_table_response = sender_stand_request.get_users_table()  # В переменную users_table_response сохраняется результат запрос на получение данных из таблицы user_model
#     str_user = user_body["firstName"] + "," + user_body["phone"] + "," + user_body["address"] + ",,," + \
#                user_response.json()["authToken"]  # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
#     assert users_table_response.text.count(str_user) == 1   # Проверка, что такой пользователь есть, и он единственный


def positive_assert(first_name):  # Функция для позитивной проверки
    user_body = get_user_body(first_name)  # В переменную user_body сохраняется обновленное тело запроса
    user_response = sender_stand_request.post_new_user(user_body) # В переменную user_response сохраняется результат запроса на создание пользователя:

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

def test_create_user_2_letter_in_first_name_get_success_response2():
    positive_assert("Aa")


def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400  # проверка код ответа
    assert response.json()["code"] == 400  # проверка код ответа именно теле ответа
    assert response.json()["message"] == "Имя пользователя введено некорректно. Имя может содержать только русские" \
                                         " или латинские буквы, длина должна быть не менее 2 и не более 15 символов"


def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")


def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")


def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")


def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")


def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Человек и Ко")


def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")


def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")


def negative_assert_no_first_name(user_body):
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400  # проверка код ответа
    assert response.json()["code"] == 400  # проверка код ответа именно теле ответа
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)

    assert response.status_code == 400  # проверка код ответа
    assert response.json()["code"] == 400  # проверка код ответа именно теле ответа

