from django.db import connection
from rest_framework import generics
from rest_framework.response import Response

def get_name(fk_human_id: int):
    with connection.cursor() as cur:
        cur.execute('select name, last_name from humans where isu_id=(%s)', [fk_human_id])
        return cur.fetchone()

def get_courses_teacher(teacher_id):
    with connection.cursor() as cur:
        courses = []
        cur.execute('select * from get_courses_teacher(%s)', [teacher_id])
        res = cur.fetchall()
        for c in res:
            new_item = {
                "course_id": c[0],
                "course_name": c[1],
                "subject_name": c[2],
                "term": c[3]
            }
            courses.append(new_item)
        return courses
    

def get_practice_teacher(teacher_id):
    with connection.cursor() as cur:
        practice = []
        cur.execute('select * from get_practice_teacher(%s)', [teacher_id])
        res = cur.fetchall()
        for c in res:
            new_item = {
                "actual_group_id": c[0],
                "group_name": c[1],
                "subject_name": c[2],
                "term": c[3]
            }
            practice.append(new_item)
        return practice
    
def make_teacher_detailed(name:str, last_name:str, courses: list, practice: list) -> list:
    lec = []
    pract = []
    for c in courses:
        lec.append(c['course_id'])
    for p in practice:
        pract.append(p['actual_group_id'])
    return {
        'name': name,
        'last_name': last_name,
        'Role': 'teacher',
        'Lector': lec,
        'Mentor': pract
    }


def one_to_many_find(obj_key, obj_assoc, obj_val, obj_val_ser, obj_key_id:int, obj_assoc_fk_id_name:str,filter1:dict, filter2:dict) -> list[dict]:
    """ Function extracts an object on the other side of many to many association

    Keyword arguments:
    filter1 -- specifies search parameters for finding obj_key instance
    filter2 -- specifies search parameters for finding obj_val instance
    obj_assoc_fk_id_name -- obj_assoc model's field name which points to the obj_val
    """
    obj_key_instance = generics.get_object_or_404(obj_key, pk=obj_key_id)
    if len(filter1) != 1:
        raise ValueError("filter1 must have 1 filter")
    key_f1 = list(filter1)[0]
    filter1[key_f1] = obj_key_instance
    print(filter1)
    obj_key_obj_val = obj_assoc.objects.filter(**filter1).values()
    print(obj_key_obj_val)
    obj_val_ids = []
    for t in obj_key_obj_val:
        obj_val_ids.append(t[obj_assoc_fk_id_name])
    if len(filter2) != 1:
        raise ValueError("filter2 must have 1 filter")
    key_f2 = list(filter2)[0]
    filter2[key_f2] = obj_val_ids
    obj_val_instances = obj_val.objects.filter(**filter2)
    ser = obj_val_ser(obj_val_instances, many=True)
    out_d = ser.data
    return out_d
