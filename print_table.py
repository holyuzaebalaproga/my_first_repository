import csv
import re
import os
from prettytable import PrettyTable


def csv_reader(file_name):
    """
    Принимает имя csv файла. Возвращает кортеж, где первый элемент - лист заголовков файла, второй - лист листов
    со строками файла

    Args:
        file_name(str): Имя файла
    Returns:
        tuple:
            list(str): лист заголовков файла
            list(list(str)): лист листов с значениями строк файла
    """
    file_lines = []
    with open(file_name, encoding="utf-8-sig") as f:
        file_reader = csv.reader(f)
        for i in file_reader:
            file_lines.append(i)
    name_row = file_lines.pop(0)
    return (name_row, file_lines)


def csv_filer(reader, list_naming):
    """
    Работает с каждым элементом листа листов, где каждый лист  - информация о професии(вакансии). Удаляет лист, если в нем
    есть пустое значение. Для каждого листа с профессией создает словарь, где ключ - определение элемента информации,
    взятый из листа с заголовками, значение - значение данной профессии. Для ключа key_skills значение - лист. Очищает
    значения от html-тегов, двойных и более пробелов. Заменяет bool-значения на русские аналоги. Возвращает лист
    словарей.

    Args:
        reader(list(list(str)): Лист листов со значениями строк csv-файла
        list_naming(list(str)): Заголовки csv-файла
    Returns:
        list(dict(Any, list[str] | str)): Список словарей каждой вакансии
    """
    vacancies_all = []
    for i in reader:  # берем 1 лист-строчку
        if len(list_naming) == len(i) and '' not in i:
            vacancies_all.append(i)  # сохраняем этот лист-строчку

    vacancies = []
    for line in vacancies_all:  # берем 1 лист-строчку
        dict_vacan = {}

        for i in range(len(list_naming)):  # проходимся по всем значениям листа-строчки
            values = []
            if line[i].find("\n") != -1:  # если есть перенос строки
                for j in line[i].split("\n"):
                    s = " ".join(re.sub(r"<[^>]+>", "", j).split())
                    values.append(s.strip())
            else:  # если нет переноса строк
                if line[i].lower() == 'false':
                    line[i] = 'Нет'
                elif line[i].lower() == 'true':
                    line[i] = 'Да'
                values = re.sub(r"<[^>]+>", "", line[i])  # очищаем значение от тегов
            dict_vacan[list_naming[i]] = values  # имя: очищенное значение
        vacancies.append(dict_vacan)  # добавляем в лист мини-словарик профессии
    return vacancies  # лист словарей


def print_vacancies(data_vacancies, dic_naming):
    """
    Переводит ключи словарей на русский, исп. словарь, принимаемый в кач-ве аргумента. Добавляет в начало каждого
    словаря пару: №: порядковый номер вакансии. Оформляет оклад в виде: "нижняя граница вилки оклада - верхняя граница
    вилки оклада валюта (С вычетом налогов или без)". Убирает время публикации, оформляет дату в виде дд.мм.ггг. Каждый
    навык выводит с новой строки через запятую. Форматирует словари, исп. функцию formatter. Печатает вакансии в виде
    таблицы, где ключи словарей - заголовки, каждая вакансия - новая строчка.

    Args:
        data_vacancies(list(dict(Any, list[str] | str))): Список словарей вакансий
        dic_naming(dict(str, str)): Словарь перевода ключей на русский

    Print:
        Таблица, где ключи словарей - заголовки, каждая вакансия - новая строчка.
    """
    rus_vacancies = []
    for i in range(len(data_vacancies)):  # i - номер словарика в data_vacancies
        rus_dict = {}
        for key, value in data_vacancies[i].items():  # пара ключ-значение
            if key in dic_naming:
                rus_dict[dic_naming[key]] = value
        rus_vacancies.append(rus_dict)  # заменены все ключи на русские

    new_vac = []
    for i in range(len(rus_vacancies)):  # i - номер словарика в rus_vacancies
        oclad = []
        d = {'№': str(i + 1)}
        for key, value in rus_vacancies[i].items():  # пара ключ-значение
            if not isinstance(value, list):
                value = " ".join(value.split())
            if key == 'Нижняя граница вилки оклада' or key == 'Верхняя граница вилки оклада' or key == 'Оклад указан до вычета налогов':
                if value == 'Да':
                    oclad.append('Без вычета налогов')
                if value == 'Нет':
                    oclad.append('С вычетом налогов')
                else:
                    oclad.append(value)
                continue
            if key == 'Идентификатор валюты оклада':
                high = " ".join(
                    [str(int(float(oclad[1])))[::-1][i:i + 3] for i in range(0, len(str(int(float(oclad[1])))), 3)])[
                       ::-1]
                low = " ".join(
                    [str(int(float(oclad[0])))[::-1][i:i + 3] for i in range(0, len(str(int(float(oclad[0])))), 3)])[
                      ::-1]  # string
                d['Оклад'] = f'{low} - {high} ({value}) ({oclad[2]})'
                continue  # Либо флаг, проверить
            if key == 'Дата и время публикации вакансии':
                d['Дата публикации вакансии'] = '.'.join(list(reversed(value[:10].split('-'))))
                continue
            if key == 'Навыки':
                value = ', '.join(value)
                d[key] = '\n'.join(str(value) for value in value.split(', '))
                continue
            d[key] = value
        new_vac.append(d)

    final_vac = []
    for i in new_vac:
        final_vac.append(formatter(i))

    x = PrettyTable(hrules=1)

    width_dic = {}
    if len(list(final_vac[0].keys())) > 0:
        for i in list(final_vac[0].keys()):
            width_dic[i] = 20

    x._max_width = width_dic
    x.align = "l"
    x.field_names = list(final_vac[0].keys())
    for i in range(len(final_vac)):
        x.add_row(list(final_vac[i].values()))
    print(x)


def formatter(row):  # работа с ОДНИМ словариком
    """
    Работает с одним словарем. Сокращает значения до 100 символов, добавляя "...". Опыт работы переводит на русский
    с помощью словаря exper_rus. Аналогично с валютой, исп. словарь currency_rus.

    Args:
        row (dict(Any, list[str] | str)): Словарь для вакансии
    Returns:
        row (dict(Any, list[str] | str)): Обработанный словарь вакансии
    """
    exper_rus = {'noExperience': 'Нет опыта', 'between1And3': 'От 1 года до 3 лет', 'between3And6': 'От 3 до 6 лет',
                 'moreThan6': 'Более 6 лет'}
    currency_rus = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари",
                    "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары",
                    "UZS": "Узбекский сум"}
    new_row = {}
    for key, value in row.items():  # берем 1 парочку
        if len(list(value)) >= 100:
            corr_v = value[:100] + '...'
            new_row[key] = corr_v
        elif key == 'Оклад':
            corr_v = value
            for k, v in currency_rus.items():
                if value.find(k) > 0:
                    corr_v = value.replace(k, v)
            new_row[key] = corr_v
        elif key == 'Опыт работы':
            if value in exper_rus:
                new_row[key] = exper_rus[value]
        else:
            new_row[key] = value
    return new_row


def get_table():
    """
    Используя csv-файл, проверяет наличие в нем данных. Если в файле нет строк, выводит "Пустой файл". Если в файле
    одна строка, выводит "Нет данных". Иначе запускает функцию print_vacancies.

    returns:
        str | print_vacancies
    """
    my_file = 'vacancies.csv'
    if os.stat(my_file).st_size == 0:
        print('Пустой файл')
    else:
        rdr = csv_reader(my_file)
        file_lines = rdr[1]
        name_row = rdr[0]
        if len(file_lines) > 0:
            vacancies = csv_filer(file_lines, name_row)

            eng_dic = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки',
                       'experience_id': 'Опыт работы',
                       'premium': 'Премиум-вакансия', 'employer_name': 'Компания',
                       'salary_from': 'Нижняя граница вилки оклада',
                       'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
                       'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
                       'published_at': 'Дата и время публикации вакансии'}
            print_vacancies(vacancies, eng_dic)
        else:
            print('Нет данных')


if __name__ == '__main__':
    get_table()