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
def addition():
    return 1 + 30
