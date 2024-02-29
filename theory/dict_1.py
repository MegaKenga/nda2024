# дан словарь в котором ключ - логин, а значение - словарь с именем и фамилией пользователя:
data = {
    "vlad_pe": {
        "firstName": "Vladimir",
        "secondName": "Petrov"
    },
    "serg_iv": {
        "firstName": "Sergey",
        "secondName": "Ivanov"
    },
    "igo_no": {
        "firstName": "Igor",
        "secondName": "Novikov"
    },
    "igo_pe": {
        "firstName": "Igor",
        "secondName": "Petrov"
    },
    "unknown_de": {
        "secondName": "Denisov"
    }
}

# надо:
# 0. Написать код (функцию, в одну линию....) которая форматирует этот словарь в список объектов по типу такого:
# [
#   {"login": "vlad_pe",  "firstName": "Vladimir", "secondName": "Petrov"},
#   {"login" : "serg_iv", "firstName": "Sergey", "secondName": "Ivanov" },
#   ...
# ]
# 1. Написать функцию которая принимает строку firstName и выдает secondName пользователя
# 2. Написать код (функцию, или лист-компрехеншн) которая выводит список всех фамилий (список должен содержать только уникальные фамилии)
# 3. Написать код, который выводит словарь формата:
# {
#     "Igor": 2,
#     "Vladimir": 1
#     ...
# }
# где ключ - имя, значение количество людей с таким именем

from collections import Counter


def data_list(data):
    d_list = []
    for login, info in data.items():
        login_info = ('login', login)
        for x in info.items():
            d_list.append(login_info)
            d_list.append(x)
        print(dict(d_list))


data_list(data)


def second_name(data):
    second_names = []
    for second_name in data.values():
        second_names.append(second_name['secondName'])
    print(list(set(second_names)))


second_name(data)


def names_list(data):
    names = []
    for first_names in data.values():
        name = first_names.get('firstName')
        if name is not None:
            names.append(name)
    x = Counter(names)
    print(dict(x))


names_list(data)
