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
        # ОК, мы имеем кортеж
        login_info = ('login', login)
        for x in info.items():
            # Тут мы вставляем этот кортеж в наш массив, но зачем-то делаем это в цикле?
            # Те этот кортеж будет вставлен несколько раз, смотря сколько осталось items в info.
            d_list.append(login_info)
            # теперь вставляем кортежи ("firstName", ""Vladimir") ("lastName", "Petrov")
            d_list.append(x)
        # тут мы имеем массив с кортежами, причем ('login', 'vlad_pe') дважды,;
        # [('login', 'vlad_pe'), ('firstName', 'Vladimir'), ('login', 'vlad_pe'), ('secondName', 'Petrov')
    # далее мы добавляем по 4 элемента (имя, фамилия и логин дважды) для каждого data.items()
    # да, ты можешь из такого списка кортежей сделать словарь методом dict(), но левый элемент кортежа (ключ) дублируется и в итоге из всех "людей"
    # в итоговом словаре будет только один логин, только одно имя и только одна фамилия,
    # print(dict(d_list))

data_list(data)

# опция первая (лист компрехеншн)
def format_data_to_list1():
    return [{"login": key, **value} for key, value in data.items()]

# то же самое через цикл for
def format_data_to_list2():
    persons = []
    for key, value in data.items():
        persons.append({"login": key, **value})
    return persons



def second_name(data):
    second_names = []
    # отлично! Единственное замечание имя переменной second_name, в этой переменное лежит что-то другое.
    # Я бы назвал ее person_data например
    for last_name in data.values():
        second_names.append(last_name['secondName'])
    print(list(set(second_names)))

# сможешь эту же задачу решить через "лист компрехенш" в одну строчку как format_data_to_list1?

def second_name(data):
    second_names =[set(last_name['secondName'] for last_name in data.values())]
    print(second_names)

second_name(data)

# second_name(data)


def names_list(data):
    names = []
    # задача решена, это хорошо. Лично я бы решил чуток по другому:
    # 1. переименовал переменную first_names которая хранит что-то другое
    # 2. постарался бы не испоьлзовать сторонних библиотек и импортов без особой неоходимости
    # это "вкусовщина" но ниже мое решение, просто для примера.
    for first_names in data.values():
        name = first_names.get('firstName')
        if name is not None:
            names.append(name)
    x = Counter(names)
    print(dict(x))


# names_list(data)


def name_list2():
    output = {}
    for person in data.values():
        first_name = person.get('firstName', None)
        if first_name is None:
            continue
        current_name_count = output.get(first_name, 0)
        output[first_name] = current_name_count + 1
    return output

name_list2()