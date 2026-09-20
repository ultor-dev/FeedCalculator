import json
import os
from dataclasses import dataclass, asdict

DATA_FILE = "animal.json"

@dataclass
class Animal:
    species: str        # вид животного
    daily_rate: float   # суточная норма корма на одну голову (кг)
    count: int          # общее поголовье


def inputInt(prompt: str, min_value: int = 1) -> int:
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


def inputFloat(prompt: str, min_value: float = 0.0) -> float:
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


def inputYesNo(prompt: str) -> bool:
    """Запрашивает ответ да/нет с проверкой корректности ввода."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("д", "да", "y", "yes", "ооба", "оба"):
            return True
        elif answer in ("н", "нет", "n", "no", "жок"):
            return False
        else:
            print("Ошибка: введите 'д'/'да'/'ооба' (да) или 'н'/'нет'/'жок' (нет).")


def showMenu() -> str:
    """Показывает главное меню и возвращает выбор пользователя."""
    print("\nРасчет потребности в кормах")
    print("~" * 30)
    print("1. Добавить один вид животных")
    print("2. Пакетный ввод нескольких видов")
    print("3. Показать список животных")
    print("4. Удалить вид животных")
    print("5. Рассчитать потребность в кормах")
    print("6. Сохранить список животных в файл")
    print("7. Загрузить список животных из файла")
    print("8. Сохранить отчет в файл")
    print("9. Справка")
    print("0. Выход")
    while True:
        choice = input("Выберите пункт меню: ").strip()
        if choice in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
            return choice
        print("Ошибка: введите число от 0 до 9. -_-")


def inputOneAnimal() -> Animal:
    """Запрашивает данные по одному виду животных."""
    species = input("Вид животного (например, корова): ").strip()
    daily_rate = inputFloat("Суточная норма корма на 1 голову (кг): ", min_value=0.01)
    count = inputInt("Поголовье (шт.): ", min_value=1)
    return Animal(species=species, daily_rate=daily_rate, count=count)


def inputAnimalsBatch() -> list[Animal]:
    """Пакетный ввод нескольких видов животных подряд."""
    animals: list[Animal] = []
    count_species = inputInt("Сколько видов животных добавить? ")

    for i in range(count_species):
        print(f"\n~~~ Животное #{i + 1} из {count_species} ~~~")
        animals.append(inputOneAnimal())

    print(f"\n[OK] Успешно добавлено видов: {len(animals)}")
    return animals


def showAnimals(animals: list[Animal]) -> None:
    """Выводит текущий список животных."""
    if not animals:
        print("\nСписок животных пуст. -_-")
        return

    print("\n" + "~" * 50)
    print(f"{'№':<4}{'Вид':<20}{'Норма/гол (кг)':<18}{'Поголовье':<10}")
    print("~" * 50)
    for i, a in enumerate(animals, start=1):
        print(f"{i:<4}{a.species:<20}{a.daily_rate:<18}{a.count:<10}")
    print("~" * 50)


def deleteAnimal(animals: list[Animal]) -> None:
    """Удаляет вид животных из списка по номеру."""
    if not animals:
        print("\nСписок животных пуст, удалять нечего. -_-")
        return

    showAnimals(animals)
    index = inputInt(f"Введите номер для удаления (1-{len(animals)}): ", min_value=1)

    if index > len(animals):
        print("Ошибка: такого номера нет в списке. :(")
        return

    removed = animals.pop(index - 1)
    print(f"[OK] Удалено: {removed.species}")


def saveAnimals(animals: list[Animal], filename: str = DATA_FILE) -> None:
    """Сохраняет список животных в JSON-файл."""
    data = [asdict(a) for a in animals]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Данные сохранены в файл '{filename}'.")


def loadAnimals(filename: str = DATA_FILE) -> list[Animal]:
    """Загружает список животных из JSON-файла, если он существует."""
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не найден. -_-")
        return []

    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    animals = [Animal(**item) for item in data]
    print(f"[OK] Загружено видов животных: {len(animals)}.")
    return animals


def calculateTotalFeed(animals: list[Animal], days: int) -> dict[str, float]:
    """Рассчитывает потребность в кормах за период для каждого вида животных."""
    result: dict[str, float] = {}
    for animal in animals:
        total_for_species = animal.daily_rate * animal.count * days
        result[animal.species] = result.get(animal.species, 0.0) + total_for_species
    return result


def printResults(result: dict[str, float], days: int) -> None:
    """Выводит итоговый отчет по потребности в кормах."""
    print(f"\nПотребность в кормах за {days} дн.:")
    print("~" * 40)

    total_all = 0.0
    for species, total in result.items():
        print(f"{species:<20} {total:>10.2f} кг")
        total_all += total

    print("~" * 40)
    print(f"{'ИТОГО по ферме:':<20} {total_all:>10.2f} кг")


def saveReport(result: dict[str, float], days: int) -> None:
    """Сохраняет итоговый отчет по кормам в текстовый файл."""
    filename = input("Введите имя файла для отчета (например, report.txt): ").strip()
    if not filename:
        filename = "feed_report.txt"

    total_all = sum(result.values())
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Потребность в кормах за {days} дн.\n")
        f.write("~" * 40 + "\n")
        for species, total in result.items():
            f.write(f"{species:<20} {total:>10.2f} кг\n")
        f.write("~" * 40 + "\n")
        f.write(f"{'ИТОГО по ферме:':<20} {total_all:>10.2f} кг\n")
    print(f"[OK] Отчет сохранен в файл '{filename}'.")


def showHelp() -> None:
    """Выводит справку по программе."""
    print("\n" + "~" * 50)
    print("СПРАВКА ПО ПРОГРАММЕ")
    print("~" * 50)
    print("Программа рассчитывает потребность в кормах на ферме.")
    print("Для каждого вида животных хранятся: название, суточная")
    print("норма корма на голову (кг) и поголовье.")
    print()
    print("Формула расчета:")
    print("  Total = норма_i * поголовье_i * дни, для каждого вида i")
    print()
    print("Пример:")
    print("  10 коров по 25 кг/сут на 7 дней => 1750 кг.")
    print("~" * 50)


def main():
    animals: list[Animal] = []
    last_result: dict[str, float] | None = None
    last_days: int | None = None

    while True:
        choice = showMenu()

        if choice == "0":
            print("\nПрограмма завершена. ^_^")
            break

        elif choice == "1":
            print("\n<~~ ДОБАВЛЕНИЕ ОДНОГО ВИДА ЖИВОТНЫХ ~~>")
            animals.append(inputOneAnimal())
            print("[OK] Вид животных добавлен.")

        elif choice == "2":
            print("\n<~~ ПАКЕТНЫЙ ВВОД ЖИВОТНЫХ ~~>")
            animals.extend(inputAnimalsBatch())

        elif choice == "3":
            showAnimals(animals)

        elif choice == "4":
            deleteAnimal(animals)

        elif choice == "5":
            if not animals:
                print("\nСначала добавьте хотя бы один вид животных. -_-")
                continue
            days = inputInt("\nНа сколько дней рассчитать корма? ")
            last_result = calculateTotalFeed(animals, days)
            last_days = days
            printResults(last_result, last_days)

        elif choice == "6":
            if not animals:
                print("\nСписок животных пуст, нечего сохранять. -_-")
                continue
            saveAnimals(animals)

        elif choice == "7":
            loaded = loadAnimals()
            if loaded:
                if inputYesNo("Заменить текущий список загруженным? (д/н): "):
                    animals = loaded
                else:
                    animals.extend(loaded)

        elif choice == "8":
            if last_result is None:
                print("\nСначала выполните расчет (пункт 5), а потом сохраняйте отчет. -_-")
            else:
                saveReport(last_result, last_days)

        elif choice == "9":
            showHelp()

        input("\nНажмите Enter для продолжения...")


if __name__ == "__main__":
    main()