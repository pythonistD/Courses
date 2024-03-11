from faker import Faker
import numpy as np
import random


def generate_humans(number_of_humans: int) -> None:
    fake = Faker('ru_RU')
    s = 'insert into humans (name, last_name) values\n'
    names = []
    for i in range(number_of_humans):
        res = fake.name().split(' ')
        s_to_add = '    ' + f'(\'{res[0]}\', \'{res[1]}\')'
        if i == number_of_humans-1:
            s_to_add += ';\n\n'
        else:
            s_to_add += ','
        names.append(s_to_add)
    vals = '\n'.join(names)
    res= s + vals
    with open('docs/generated_humans.pgsql', 'a', encoding='utf-8') as f:
        f.write(res)

dep_cur = {
    'ПИКТ': ['СППО', 'Нейротехнологии и программирование', 
             'Компьютерные технологии в дизайне', 'Компьютерные системы и технологии'],
    'БИТ': ['Технологии защиты информации', 
            'Безопасность систем искусственного интелекта', 'Информационная безопасность'],
    'СУиР': ['Мехатроника и робототехника', 'Приборостоение', 
             'Автоматизация технологических процессов и производств', 'Электроэнергетика и электротехника']
}
dep_gr = {
    'ПИКТ': 'P',
    'БИТ': 'B',
    'СУиР': 'S'
}
def generate_group_name(dep: str, course: int):
    tail = random.randint()

def generate_students(dep:str, cur:int, course:int, groups:list, humans_ids: list) -> None:
    students = []
    spaces = '    '
    insert_line = 'insert into student (fk_human_id, course, group_name, department, curriculum) values\n'
    head = dep_gr[dep] + str(cur) + str(course)
    for i in range(len(humans_ids)):
        gr = head + random.choice(groups)
        res = spaces + f'({humans_ids[i]}, {course}, \'{gr}\', \'{dep}\', \'{dep_cur[dep][cur]}\')'
        if i == len(humans_ids)-1:
            res += ';\n\n'
        else:
            res += ','
        students.append(res)
    query = insert_line + '\n'.join(students)
    with open('docs/generated_students.pgsql', 'a', encoding='utf-8') as f:
        f.write(query)

def generate_teacher(dep:str, humans_ids: list) -> None:
    teachers = []
    spaces = '    '
    insert_line = 'insert into teacher (fk_humans_id, department) values\n'
    for i in range(len(humans_ids)):
        res = spaces + f'({humans_ids[i]}, \'{dep}\')'
        if i == len(humans_ids)-1:
            res += ';\n\n'
        else:
            res += ','
        teachers.append(res)
    query = insert_line + '\n'.join(teachers)
    with open('docs/generated_teachers.pgsql', 'a', encoding='utf-8') as f:
        f.write(query)


hum_ids = np.arange(108, 113)
print(hum_ids)
generate_students('ПИКТ', 3, 2, ['111'],  [121, 122])
#generate_teacher('ПИКТ', hum_ids)
#generate_humans(10)