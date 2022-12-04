import csv
import re


def csv_reader(file_name):
    file_lines = []
    with open(file_name, encoding="utf-8-sig") as f:
        file_reader = csv.reader(f)
        for i in file_reader:
            file_lines.append(i)
    name_row = file_lines.pop(0)
    return (name_row, file_lines)


# file_name = input()

def csv_filer(reader, list_naming):
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
    rus_vacancies = []
    for i in range(len(data_vacancies)):  # i - номер словарика в data_vacancies
        rus_dict = {}
        for key, value in vacancies[i].items():  # пара ключ-значение
            if key in dic_naming:
                rus_dict[dic_naming[key]] = value
        rus_vacancies.append(rus_dict)

    for i in range(len(rus_vacancies)):
        for key, value in rus_vacancies[i].items():
            if isinstance(value, list):
                print(f'{key}: {", ".join(value)}')
            else:
                print(f'{key}: {" ".join(value.split())}')
        print()


rdr = csv_reader('vacancies.csv')
file_lines = rdr[1]
name_row = rdr[0]
vacancies = csv_filer(file_lines, name_row)
eng_dic = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы',
           'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Нижняя граница вилки оклада',
           'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов',
           'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона',
           'published_at': 'Дата и время публикации вакансии'}
print_vacancies(vacancies, eng_dic)
