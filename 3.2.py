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


def csv_filer(reader, list_naming):
    vacancies_all = []
    for i in reader: #берем 1 лист-строчку
        if len(list_naming) == len(i) and '' not in i: #сохраняем только те строчки, где нет пустых пунктов и подходящая длина
            vacancies_all.append(i) #сохраняем этот лист-строчку

    vacancies = []
    for line in vacancies_all: #чистим лист от тэгов, превращаем /n в лист, меняем true/false на русское
        dict_vacan = {}
        for i in range(len(list_naming)): #проходимся по всем значениям листа-строчки
            values = []
            if line[i].find("\n") != -1: #если есть перенос строки
                for j in line[i].split("\n"):
                    s = " ".join(re.sub(r"<[^>]+>","",j).split())
                    values.append(s.strip())
            else: #если нет переноса строк
                if line[i].lower()=='false':
                    line[i] = 'Нет'
                elif line[i].lower()=='true':
                    line[i] = 'Да'
                values = re.sub(r"<[^>]+>","",line[i]) #очищаем значение от тегов
            dict_vacan[list_naming[i]] = values  #имя: очищенное значение
        vacancies.append(dict_vacan) #добавляем в лист мини-словарик профессии    
    return vacancies #лист словарей

def print_vacancies(data_vacancies, dic_naming):
    rus_vacancies = []
    for i in range(len(data_vacancies)): #i - номер словарика в data_vacancies
        rus_dict = {}
        for key, value in vacancies[i].items(): #пара ключ-значение
            if key in dic_naming:
                rus_dict[dic_naming[key]] = value
        rus_vacancies.append(rus_dict)

    new_vac = []
    for i in range(len(rus_vacancies)): #i - номер словарика в rus_vacancies
        oclad = []
        d = {}
        for key, value in rus_vacancies[i].items():#пара ключ-значение
            if key=='Нижняя граница вилки оклада' or key== 'Верхняя граница вилки оклада' or key== 'Оклад указан до вычета налогов':
                if value=='Да':
                    oclad.append('Без вычета налогов')
                if value=='Нет':
                    oclad.append('С вычетом налогов')
                else:
                    oclad.append(value)
                continue
            if key=='Идентификатор валюты оклада':
                high = " ".join([str(int(float(oclad[1])))[::-1][i:i+3] for i in range(0, len(str(int(float(oclad[1])))), 3)])[::-1]
                low = " ".join([str(int(float(oclad[0])))[::-1][i:i+3] for i in range(0, len(str(int(float(oclad[0])))), 3)])[::-1]
                
                d['Оклад'] = f'{low} - {high} ({value}) ({oclad[2]})'
                continue #Либо флаг, проверить
            if key=='Дата и время публикации вакансии':
                d['Дата публикации вакансии'] = '.'.join(list(reversed(value[:10].split('-'))))
                continue
            d[key] = value
        new_vac.append(d)
    
    final_vac = []
    for i in new_vac:
        final_vac.append(formatter(i))


    for i in range(len(final_vac)): #печатаем
        for key, value in final_vac[i].items():
            if isinstance(value,list):
                print(f'{key}: {", ".join(value)}')
            else:
                print(f'{key}: {" ".join(value.split())}')
        print()


def formatter(row): #работа с ОДНИМ словариком
    exper_rus = {'noExperience': 'Нет опыта', 'between1And3': 'От 1 года до 3 лет', 'between3And6': 'От 3 до 6 лет', 'moreThan6': 'Более 6 лет'}
    currency_rus = {"AZN": "Манаты", "BYR": "Белорусские рубли", "EUR": "Евро", "GEL": "Грузинский лари", "KGS": "Киргизский сом", "KZT": "Тенге", "RUR": "Рубли", "UAH": "Гривны", "USD": "Доллары", "UZS": "Узбекский сум"}
    new_row = {}
    for key, value in row.items(): #берем 1 парочку        
        if key=='Оклад':
            corr_v = value
            for k, v in currency_rus.items():
                if value.find(k)>0:
                    corr_v = value.replace(k, v)
            new_row[key] = corr_v
        elif key=='Опыт работы':
            if value in exper_rus:
                new_row[key] = exper_rus[value]
        else:
            new_row[key] = value          
    return new_row
            
rdr = csv_reader('vacancies.csv')
file_lines = rdr[1]
name_row = rdr[0]
vacancies = csv_filer(file_lines, name_row)
eng_dic = {'name': 'Название', 'description': 'Описание', 'key_skills': 'Навыки', 'experience_id': 'Опыт работы', 'premium': 'Премиум-вакансия', 'employer_name': 'Компания', 'salary_from': 'Нижняя граница вилки оклада', 'salary_to': 'Верхняя граница вилки оклада', 'salary_gross': 'Оклад указан до вычета налогов', 'salary_currency': 'Идентификатор валюты оклада', 'area_name': 'Название региона', 'published_at': 'Дата и время публикации вакансии'}
print_vacancies(vacancies, eng_dic)