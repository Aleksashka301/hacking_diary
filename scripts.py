import os
import django
import argparse
import random
from django.core.exceptions import ObjectDoesNotExist


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()


from datacenter.models import Schoolkid, Mark, Chastisement, Commendation


def change_ratings(name_student):
    student_marks = Mark.objects.filter(schoolkid=name_student, points__in=[2, 3])
    for mark in student_marks:
        mark.points = random.choice([4, 5])
        mark.save()


def delete_comments(name_student):
    comments_bad = Chastisement.objects.filter(schoolkid=name_student)
    for comment in comments_bad:
        comment.delete()


def add_comment(name_student, subject, commentary):
    last_mark = Mark.objects.filter(
        schoolkid=name_student,
        subject__title=subject,
        points=5
    )
    last_mark = last_mark.order_by('-created').first()

    teacher = last_mark.teacher
    created_date = last_mark.created
    subject = last_mark.subject

    Commendation.objects.create(
        text=commentary,
        created=created_date,
        schoolkid=name_student,
        teacher=teacher,
        subject=subject
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('name_student', type=str)
    parser.add_argument('subject', type=str)
    parser.add_argument('commentary', nargs='?', default='Отличная работа!', type=str)
    args = parser.parse_args()

    name_student = args.name_student
    commentary = args.commentary
    subject = args.subject

    try:
        student = Schoolkid.objects.get(full_name=name_student)
        change_ratings(student)
        delete_comments(student)
        add_comment(student, subject, commentary)
    except ObjectDoesNotExist:
        print(f'Ученика с именем {name_student} в базе данных нет, либо вы ввели имя не полностью.')
    except AttributeError:
        print(f'Предмета {subject} не существует либо он записан не верно.')

