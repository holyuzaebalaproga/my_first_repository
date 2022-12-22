from print_as_OOP import get_OOP
from print_table import get_table



def main_function():
    """
    Функция для запуска всей программы. При запуске просит ввести пользователя тип вывода вакансий. При вводе "ООП" запускает
    функцию печати вакансий как объекта ООП, используя функцию из файла print_as_OOP. При вводе "Таблица" запускает
    функцию печати вакансий в виде таблицы, исп. функцию из файла print_table.
    """
    main_input = input('Введите тип вывода вакансий(ООП или Таблица): ')
    if main_input != "ООП" and main_input != "Таблица":
        print("Введён неправильный тип вывода")
        return
    if main_input == "ООП":
        get_OOP()
    else:
        get_table()


if __name__ == '__main__':
    main_function()