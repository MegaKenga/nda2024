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

dict3 = {
    "tomato": 8,
    "banana": "1",
    "kiwi": "many"
}

# задача решалась во втором файлике, но теперь она усложнена:
# нужно написать код который принимает один, два или сколько угодно словарей типа вверху и объединяет значения и выводит словарь с сумарными значениями.
# пусть значение может быть строкой, например {"banana": "200"} и это тоже будет работать
# если строка не совместимая со сложением {"banana": "a lot"} ее игнорируем


def dict_intersection(*args):
    united_dict = dict()
    for arg in args:
        for key, value in arg.items():
            try:
                quantity = int(value)
            except (TypeError, ValueError):
                continue
            if key in united_dict:
                united_dict[key] += quantity
            elif key not in united_dict:
                united_dict.update({key: quantity})

    return united_dict


print(dict_intersection(dict1, dict2, dict3))
