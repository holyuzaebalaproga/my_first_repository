from print_as_OOP import get_OOP
from print_table import get_table



def main_function():
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