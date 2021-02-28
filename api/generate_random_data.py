import datetime
import logging
import os
import random

from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

from api.models import UniversityAdmin, University, Department, Year, FieldOfStudy, Subject, DepartmentAdmin, Student, \
    Points

if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    get_user_model().objects.all().delete()
    for w in range(2):
        logging.info(f'Generating university {w}')
        university_admin_user = get_user_model()(username=f'university_admin{w}',
                                                 email=f'university_admin{w}@gmail.com')
        university_admin_user.set_password('pass')
        university_admin_user.save()
        university_admin = UniversityAdmin.objects.create(user=university_admin_user)
        university = University.objects.create(university_admin=university_admin, name=f'university{w}')

        for j in range(2):
            logging.info(f'Generating department {j}')
            department = Department.objects.create(university=university, name=f'department{j}')

            for n in range(2):
                logging.info(f'Generating department admin {n}')
                department_admin_user = get_user_model()(username=f'department_admin{department.id}{n}',
                                                         email=f'department_admin{department.id}{n}@gmail.com')
                department_admin_user.set_password('pass')
                department_admin_user.save()
                DepartmentAdmin(user=department_admin_user, department=department).save()

            for k in range(2):
                logging.info(f'Generating year {k}')
                year = Year.objects.create(department=department, start_year=2014 + k)

                for l in range(2):
                    logging.info(f'Generating field of study {l}')
                    field_of_study = FieldOfStudy.objects.create(year=year, name=f'field_of_study{l}')

                    for m in range(5):
                        logging.info(f'Generating subject {m}')
                        Subject(field_of_study=field_of_study, name=f'subject{year.id}{m}', description="dasdas",
                                lecturer="ssda", day='MONDAY', type='P', start_time=datetime.time(10, 33),
                                end_time=datetime.time(12, 25), limit=15).save()
                        Subject(field_of_study=field_of_study, name=f'subject{year.id}{m}', description="dasdas",
                                lecturer="ssda", day='TUESDAY', type='P', start_time=datetime.time(10, 33),
                                end_time=datetime.time(12, 25), limit=15).save()
                        Subject(field_of_study=field_of_study, name=f'subject{year.id}{m}', description="dasdas",
                                lecturer="ssda", day='FRIDAY', type='W', start_time=datetime.time(10, 33),
                                end_time=datetime.time(12, 25), limit=100).save()

                    for o in range(30):
                        logging.info(f'Generating student {o}')
                        student_user = get_user_model()(username=f'student{field_of_study.id}{o}',
                                                        email=f'student{field_of_study.id}{o}@gmail.com')
                        student_user.set_password('pass')
                        student_user.save()
                        student = Student.objects.create(field_of_study=field_of_study, user=student_user)

                        subjects_names =Subject.objects.filter(field_of_study_id=field_of_study.id, type='P').values_list(
                            'name').distinct()
                        for subject_name in subjects_names:
                            students_points_to_give = 8
                            subjects = Subject.objects.filter(field_of_study=field_of_study, type='P',
                                                              name=subject_name[0])
                            for (w, subject) in enumerate(subjects):
                                logging.info(f'Generating points: student {o} subject {subject.id}')
                                if students_points_to_give == 0:
                                    break
                                if w == len(subjects) - 1:
                                    Points(student=student, subject=subject,
                                           points=students_points_to_give).save()
                                    break
                                points_given = random.randint(1, students_points_to_give)
                                Points(student=student, subject=subject,
                                       points=points_given).save()
                                students_points_to_give -= points_given
