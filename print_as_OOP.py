import csv
import re
from var_dump import var_dump


class DataSet(object):
    """
    Класс для представления основного объекта данных в виде списка вакансий и имени csv файла.
    Attributes:
        file_name(str): Имя csv файла
        vacancies_objects(list): Лист из объектов-вакансий
    """
    def __init__(self, name, listik):
        """
        Инициализирует объект Datset.
        Args:
            file_name(str): Имя csv файла
            vacancies_objects(list): Лист из объектов-вакансий
        """
        self.file_name = name
        self.vacancies_objects = listik


class Vacancy(object):
    """
    Класс для представления вакансии.

    Attributes:
        name(str): Имя вакансии(профессии)
        description(str): Описание
        key_skills(list): Список ключевых кавыков
        experience_id(str): Опыт работы
        premium(str): Премиум-вакансия или нет
        employer_name(str): Имя компании работодателя
        salary(object): Объект Salary, состоящий из верхней, нижней вилок оклада, учетом налогов или нет и валюты
        area_name(str): Название региона
        published_at(str): Дата и время публикации
    """
    def __init__(self, name, description, key_skills, experience_id, premium, employer_name, salary, area_name,
                 published_at):
        """
        Инициализирует объект Vacanсy.

    Args:
        name(str): Имя вакансии(профессии)
        description(str): Описание
        key_skills(list): Список ключевых кавыков
        experience_id(str): Опыт работы
        premium(str): Премиум-вакансия или нет
        employer_name(str): Имя компании работодателя
        salary(object): Объект Salary, состоящий из верхней, нижней вилок оклада, учетом налогов или нет и валюты
        area_name(str): Название региона
        published_at(str): Дата и время публикации
        """
        self.name = name
        self.description = description
        self.key_skills = key_skills
        self.experience_id = experience_id
        self.premium = premium
        self.employer_name = employer_name
        self.salary = salary
        self.area_name = area_name
        self.published_at = published_at


class Salary(object):
    """
    Класс для представления зарплаты.

    Attributes:
        salary_from (str or int or float): Нижняя граница вилки оклада
        salary_to (str or int or float): Верхняя граница вилки оклада
        salary_gross(str): С вычетом налогов(TRUE или FALSE)
        salary_currency(str): Валюта оклада
    """
    def __init__(self, salary_from, salary_to, salary_gross, salary_currency):
        """
        Инициализирует объект Salary.
        Args:
            salary_from (str or int or float): Нижняя граница вилки оклада
            salary_to (str or int or float): Верхняя граница вилки оклада
            salary_gross(str): С вычетом налогов(TRUE или FALSE)
            salary_currency(str): Валюта оклада
        """
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.salary_gross = salary_gross
        self.salary_currency = salary_currency


def csv_parser(file_name):  # формируется список словарей, делает строку с n листом, убирает тэги
    """
    Формирует список словарей из заданного (имени) файла. Строку с переносом строки делает листом. Каждое значение
    очищает от html-тэгов, приводя к читаемому виду
    Returns:
        list: Лист словарей из вакансий
    """
    with open(file_name, 'r', encoding='utf-8-sig') as f:
        r_csv = csv.reader(f)
        try:
            list_naming = next(r_csv)
        except StopIteration:
            print('Пустой файл')
            exit()
        file_lines = []
        for r in r_csv:
            if all(x != '' for x in r) and (len(list_naming) == len(r)):
                file_lines.append(r)

    vacancies_all = []
    for i in file_lines:  # берем 1 лист-строчку
        if len(list_naming) == len(i) and '' not in i:
            vacancies_all.append(i)  # сохраняем этот лист-строчку
    vacancies = []
    for line in vacancies_all:  # берем 1 лист-строчку
        dict_vacan = {}
        for i in range(len(list_naming)):  # проходимся по всем значениям листа-строчки
            values = []
            if line[i].find("\n") != -1:  # если есть перенос строки
                for j in line[i].split("\n"):  # для каждого элемента разделенного n
                    s = " ".join(re.sub(r"<[^>]+>", "", j).split())  # убрать тэги и лишние пробелы
                    values.append(s.strip())
            else:  # если нет переноса строк
                values = re.sub(r"<[^>]+>", "", line[i])  # очищаем значение от тегов
                values = " ".join(values.split())
            dict_vacan[list_naming[i]] = values  # имя: очищенное значение
        vacancies.append(dict_vacan)  # добавляем в лист мини-словарик профессии
    return vacancies  # лист словарей


def get_OOP():
    """
        Просит пользователя ввести имя csv файла. Данные из файла обрабатывает и выводит в виде вакансий в ООП.
        Returns:
            object: Печатает данные в виде объектов var_dump
    """
    file_name = input('Введите название файла: ')  # 'vacancies.csv'
    # filt_input = input('Введите параметр фильтрации: ')
    # sort_param = input('Введите параметр сортировки: ')
    # sort_order = input('Обратный порядок сортировки (Да / Нет): ')
    # len_of_vac = input('Введите диапазон вывода: ').split(' ')
    # segments = input('Введите требуемые столбцы: ').split(', ')

    vacancies = csv_parser(file_name)
    vacancies_objects = []
    for d in vacancies:
        sal_obj = Salary(d['salary_from'], d['salary_to'], d['salary_gross'], d['salary_currency'])
        obj = Vacancy(d['name'], d['description'], d['key_skills'], d['experience_id'],
                      d['premium'], d['employer_name'], sal_obj, d['area_name'], d['published_at'])
        vacancies_objects.append(obj)
    data = DataSet(file_name, vacancies_objects)
    var_dump(data)

if __name__ == '__main__':
    get_OOP()