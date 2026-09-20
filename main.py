import json
import os
from dataclasses import dataclass, asdict
DATA_FILE="animal.json"

@dataclass
class Animal:
    species: str        # вид животного
    daily_rate: float   # суточная норма корма на одну голову (кг)
    count: int          # общее поголовье

def input_int(prompt: str, min_value: int = 1) -> int:
    """Запрашивает целое число с проверкой корректности ввода."""
    while True:
        try:
            value = int(input(prompt))
            if value < min_value:
                print(f"Значение должно быть не меньше {min_value}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите целое число.")

def input_float(prompt: str, min_value: float = 0.0) -> float:
    """Запрашивает вещественное число с проверкой корректности ввода."""
    while True:
        try:
            value = float(input(prompt))
            if value < min_value:
                print(f"Значение должно быть не меньше {min_value}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите число (можно с точкой, например 2.5).")

def input_yes_no(prompt: str) -> bool:
    """Запрашивает ответ да/нет с проверкой корректности ввода."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("д", "да"):
            return True
        elif answer in ("н", "нет"):
            return False
        else:
            print("Ошибка: введите 'д' (да) или 'н' (нет).")

def input_animals() -> list[Animal]:
    """Запрашивает у пользователя данные по видам животных."""
    animals: list[Animal] = []
    count_species = input_int("Сколько видов животных нужно ввести? ")

    for i in range(count_species):
        print(f"\n--- Животное #{i + 1} ---")
        species = input("Вид животного (например, корова): ").strip()
        daily_rate = input_float("Суточная норма корма на 1 голову (кг): ", min_value=0.01)
        count = input_int("Поголовье (шт.): ", min_value=1)

        animals.append(Animal(species=species, daily_rate=daily_rate, count=count))

    return animals

def save_animals(animals: list[Animal], filename: str = DATA_FILE) -> None:
    """Сохраняет список животных в JSON-файл."""
    data = [asdict(a) for a in animals]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Данные сохранены в файл '{filename}'.")


def load_animals(filename: str = DATA_FILE) -> list[Animal]:
    """Загружает список животных из JSON-файла, если он существует."""
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден. Начинаем с пустого списка.")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    animals = [Animal(**item) for item in data]
    print(f"Загружено видов животных: {len(animals)}.")
    return animals


def save_report(result: dict[str, float], days: int, filename: str = "feed_report.txt") -> None:
    """Сохраняет итоговый отчет по кормам в текстовый файл."""
    total_all = sum(result.values())
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Потребность в кормах за {days} дн.\n")
        f.write("=" * 40 + "\n")
        for species, total in result.items():
            f.write(f"{species:<20} {total:>10.2f} кг\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'ИТОГО по ферме:':<20} {total_all:>10.2f} кг\n")
    print(f"Отчет сохранен в файл '{filename}'.")

def calculate_total_feed(animals: list[Animal], days: int) -> dict[str, float]:
    """Рассчитывает потребность в кормах за период для каждого вида животных."""
    result: dict[str, float] = {}
    for animal in animals:
        total_for_species = animal.daily_rate * animal.count * days
        # если один и тот же вид введен несколько раз - суммируем
        result[animal.species] = result.get(animal.species, 0.0) + total_for_species
    return result

def print_results(result: dict[str, float], days: int) -> None:
    """Выводит итоговый отчет по потребности в кормах."""
    print("\n" + "=" * 40)
    print(f"ПОТРЕБНОСТЬ В КОРМАХ ЗА {days} ДН.")
    print("=" * 40)

    total_all = 0.0
    for species, total in result.items():
        print(f"{species:<20} {total:>10.2f} кг")
        total_all += total

    print("-" * 40)
    print(f"{'ИТОГО по ферме:':<20} {total_all:>10.2f} кг")
    print("=" * 40)
    
def main():
    print("Расчет потребности в кормах на ферме\n")

    animals: list[Animal] = []
 
    # Предлагаем загрузить ранее сохраненные виды животных
    if os.path.exists(DATA_FILE):
        if input_yes_no(f"Найден файл '{DATA_FILE}'. Загрузить сохраненные данные? (д/н): "):
            animals = load_animals()
 
    # Предлагаем добавить новые виды животных
    if input_yes_no("Добавить новые виды животных? (д/н): ") or not animals:
        animals.extend(input_animals())
 
    if not animals:
        print("Нет данных о животных. Завершение программы.")
        return
 
    # Предлагаем сохранить обновленный список
    if input_yes_no("\nСохранить список животных в файл? (д/н): "):
        save_animals(animals)
 
    days = input_int("\nНа сколько дней рассчитать корма? ")
 
    result = calculate_total_feed(animals, days)
    print_results(result, days)
 
    # Предлагаем сохранить отчет
    if input_yes_no("\nСохранить отчет в файл? (д/н): "):
        save_report(result, days)


if __name__ == "__main__":
    main()