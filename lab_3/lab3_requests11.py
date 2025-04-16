from flask import Blueprint, request, jsonify
import random

lab3_requests11 = Blueprint('lab3_requests11', __name__)

# Раздел 1. Подготовка сервера с API

@lab3_requests11.route('/number/', methods=['GET'])
def handle_number():
    param = request.args.get('param', type=float) # Получаем параметр 'param' из запроса
    
    # Проверяем, что параметр передан и является числом
    if param is None:
        return jsonify({'error': 'Parameter "param" is required and should be a number'}), 400
    
    random_number = random.random() # Генерируем случайное число от 0 до 1
    result = random_number * param # Умножаем на параметр

    # Возвращаем результат в JSON
    return jsonify({
        'random_number': random_number,
        'param': param,
        'result': result
    })

@lab3_requests11.route('/number/', methods=['POST'])
def handle_post_number():
    # Проверяем и получаем JSON из тела запроса
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400
    
    data = request.get_json()
    
    # Проверяем наличие jsonParam
    if 'jsonParam' not in data or not isinstance(data['jsonParam'], (int, float)):
        return jsonify({'error': 'Field "jsonParam" is required and must be a number'}), 400
    
    param = data['jsonParam']
    random_number = random.uniform(0, 100)  # Генерируем случайное число
    
    # Доступные операции с их обозначениями
    operations = {
        'sum': lambda a, b: a + b,
        'sub': lambda a, b: a - b,
        'mul': lambda a, b: a * b,
        'div': lambda a, b: a / b if b != 0 else None
    }
    
    chosen_operation = random.choice(list(operations.keys()))
    
    # Вычисляем результат с обработкой деления на ноль
    if chosen_operation == 'div' and param == 0:
        return jsonify({'error': 'Division by zero'}), 400
    
    result = operations[chosen_operation](random_number, param)
    
    return jsonify({
        'random_number': round(random_number, 4),
        'param': param,
        'operation': chosen_operation,
        'result': round(result, 4) if result is not None else None
    })

@lab3_requests11.route('/number/', methods=['DELETE'])
def handle_delete_number():
    # Генерируем случайное число от 1 до 100 (чтобы избежать деления на 0)
    random_number = random.uniform(1, 100)
    
    operations = {
        'sum': lambda a, b: a + b,
        'sub': lambda a, b: a - b,
        'mul': lambda a, b: a * b,
        'div': lambda a, b: a / b
    }
    chosen_operation = random.choice(list(operations.keys()))
    second_operand = random.uniform(1, 10)  # Ограничиваем диапазон для наглядности
    
    # Вычисляем результат
    result = operations[chosen_operation](random_number, second_operand)
    
    return jsonify({
        'first_operand': round(random_number, 4),
        'second_operand': round(second_operand, 4),
        'operation': chosen_operation,
        'result': round(result, 4)
    })

# Раздел 2. Отправка запросов на сервер с API

import requests

def section2_task1():
    print("GET")
    param = random.uniform(1, 10)
    print(f"Случайный параметр: {round(param, 4)}")

    response = requests.get("http://127.0.0.1:5000/number/", params={"param": param})

    if response.status_code == 200:
        data = response.json()
        print("Ответ от сервера:", data)
        return data['result']
    else:
        print("Ошибка запроса:", response.text)
        return None
    

def section2_task2():
    print(" POST ")
    param = random.uniform(1, 10)
    print(f"Случайный параметр: {round(param, 4)}")

    headers = {
        "Content-Type": "application/json"
    }
    json_data = {
        "jsonParam": param
    }

    response = requests.post("http://127.0.0.1:5000/number/", json=json_data, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Ответ от сервера:", data)
        return data['result']
    else:
        print("Ошибка запроса:", response.text)
        return None

def section2_task3():
    print(" DELETE ")

    response = requests.delete("http://127.0.0.1:5000/number/")

    if response.status_code == 200:
        data = response.json()
        print("Ответ от сервера:", data)
        return data['result']
    else:
        print("Ошибка запроса:", response.text)
        return None

def section2_task4():
    print("Финальный расчёт")
    
    res1 = section2_task1()
    res2 = section2_task2()
    res3 = section2_task3()

    if None in [res1, res2, res3]:
        print("Один из этапов вернул ошибку. Завершение.")
        return
    
    print(f"\nПромежуточные значения:\n1: {res1}\n2: {res2}\n3: {res3}")

    final_result = res1
    final_result = final_result + res2
    final_result = final_result + res3

    print(f"\nФинальное значение (float): {final_result}")
    final_result_int = int(final_result)
    print(f"Финальное значение (int): {final_result_int}")

# if __name__ == "__main__":
#     section2_task4()



