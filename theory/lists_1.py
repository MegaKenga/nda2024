a = ['alex', 'bob', 'john']
b = ['alice', 'bob', 'anna']
c = ['alex', 'bob', 'mike']

# 1. Напиши функцию которая принимает два или более массиввов как тут и выводит массив со всеми именами без пересечений.
# Не используй сет

# 2. Напиши функциою которая принимает два ли более массивов как тут и выводит только те имена которые присутствуют во всех массивах сразу

# 3. Напиши функию которая принимает массим объектов и выдает сумму чека. Это должна быть "одна линия".
GOODS = [
    {'name': 'bread',   'price': 1.00, 'quantity': 3},
    {'name': 'milk',    'price': 2.00, 'quantity': 2},
    {'name': 'gold',    'price': 8.00, 'quantity': 5},
    {'name': 'silver',  'price': 2.00, 'quantity': 4},
]

# 4. напиши функцию которая принимает массив цифр типа [1,6,3] и выдает число из этих цифр, типа 163.


def unique_names_list(*args):
    new_list = []
    for arg in args:
        for name in arg:
            if name not in new_list:
                new_list.append(name)

    return new_list


print(unique_names_list(a, b))


def names_list_intersection(*args):
    new_list = []
    counter = 1
    names_dict = dict()
    names_intersection_list = []
    for arg in args:
        for name in arg:
            new_list.append(name)
    for name in new_list:
        if name not in names_dict:
            names_dict[name] = counter
        else:
            names_dict[name] += counter
    for name, count in names_dict.items():
        if count == len(args):
            names_intersection_list.append(name)

    return names_intersection_list, names_dict


print(names_list_intersection(a, b, c))


def cheque_sum(cheque):
    total_sum = 0
    for item in cheque:
        item_sum = item['price'] * item['quantity']
        total_sum += item_sum

    return total_sum


print(cheque_sum(GOODS))


def list_add_items(items_list):
    list_string = ''
    for item in items_list:
        list_string += str(item)
    resulting_list = [int(list_string)]

    return resulting_list


print(list_add_items([1, 2, 8, 4, 5]))
