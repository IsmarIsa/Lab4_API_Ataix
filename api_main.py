import json
import requests
from tabulate import tabulate

# Загрузка конфигурации API
CONFIG_FILE = "Api.json"
BASE_URL = "https://api.ataix.kz"

def load_config():
    """Загружает API-ключ из файла конфигурации."""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        return config.get("api_key", "")
    except (FileNotFoundError, json.JSONDecodeError):
        print("Ошибка: Не удалось загрузить конфигурацию.")
        return ""

API_KEY = load_config()

def fetch_data(endpoint):
    """Отправляет GET-запрос к API и возвращает результат."""
    url = f"{BASE_URL}{endpoint}"
    headers = {"API-KEY": API_KEY, "Content-Type": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        return "Ошибка: Превышено время ожидания ответа."
    except requests.exceptions.HTTPError as err:
        return f"Ошибка HTTP: {err}"
    except requests.exceptions.RequestException as err:
        return f"Ошибка запроса: {err}"

def format_output(data):
    """Форматирует вывод в виде таблицы, если возможно."""
    if isinstance(data, list) and data and isinstance(data[0], dict):
        headers = data[0].keys()
        table = [list(item.values()) for item in data]
        return tabulate(table, headers=headers, tablefmt="grid")
    return data

def show_menu():
    """Выводит меню выбора и возвращает доступные опции."""
    menu_options = {
        "1": ("Список всех валют", "/api/currencies"),
        "2": ("Список всех торговых пар", "/api/symbols"),
        "3": ("Цены всех токенов и монет", "/api/prices"),
        "finish": ("Завершить", None)
    }
    print("\nВыберите действие:")
    for key, (desc, _) in menu_options.items():
        print(f"{key} - {desc}")
    return menu_options

if __name__ == "__main__":
    while True:
        options = show_menu()
        choice = input("Введите команду: ").strip().lower()
        
        if choice in options:
            description, endpoint = options[choice]
            if choice == "finish":
                print("Выход из программы.")
                break
            print(f"\n{description}:")
            response_data = fetch_data(endpoint)
            print(format_output(response_data))
        else:
            print("Некорректный ввод, попробуйте снова.")
