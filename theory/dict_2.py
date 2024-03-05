# есть данные тdataипа фрукт и его количество на складе например в килограммах
dict1 = {
    "apple": 100,
    "orange": 200,
    "banana": 24
}

dict2 = {
    "apple": 23,
    "kiwi": 28,
}

# нужно написать код (сделай пожалуйста 2-3 вариации, например функцию, может через одну-линию (list comprehension))
# который объединяет значения и выводит словарь с сумарными значениями.


# def dict_intersection(dict1, dict2):
#     print({k: dict1.get(k, 0) + dict2.get(k, 0) for k in set(dict1) | set(dict2)})
#
# dict_intersection(dict1, dict2)


def dict_intersection(dict1, dict2):
    united_dict = dict1

    for key, value in dict2.items():
        if key in dict1:
            united_dict[key] += value
        else:
            united_dict.update({key: value})
    print(united_dict)

dict_intersection(dict1, dict2)

# немного улучшил твое решение
def dict_intersection_2(dict1, dict2):
    united_dict = dict1
    for key, value in dict2.items():
        united_dict[key] = united_dict.get(key, 0) + value
    print(united_dict)

dict_intersection_2(dict1, dict2)