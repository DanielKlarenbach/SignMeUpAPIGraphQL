import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()
import django.contrib.auth as djc_auth

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, SubjectType, \
    Subject, Student, Points


def generate_time():
    minutes = ['00', '15', '30', '45']
    time = str(random.randint(8, 18)) + ':' + random.choice(minutes)
    return time


def generate_day():
    days = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']
    return random.choice(days)


if __name__ == '__main__':
    djc_auth.get_user_model().objects.all().delete()

    university_admin_user = djc_auth.get_user_model()(username="university_admin",
                                                      email="university_admin@gmail.com")
    university_admin_user.set_password('pass')
    university_admin_user.save()

    university_admin = UniversityAdmin.objects.create(user=university_admin_user)

    university = University.objects.create(university_admin=university_admin, name='university')

    for department_num in range(3):
        department = Department.objects.create(university=university, name=f'department{department_num}')

        for department_admin_num in range(3):
            department_admin_user = djc_auth.get_user_model()(
                username=f'department_admin{department_num}{department_admin_num}',
                email=f'department_admin{department_num}{department_admin_num}@gmail.com')
            department_admin_user.set_password('pass')
            department_admin_user.save()

            department_admin = DepartmentAdmin.objects.create(user=department_admin_user,
                                                              department=department)

        for start_year in range(2016, 2019):
            year = Year.objects.create(start_year=start_year, department=department)

            for field_of_study_num in range(3):
                field_of_study = FieldOfStudy.objects.create(year=year,
                                                             name=f'field_of_study{department_num}{field_of_study_num}')

                for subject_type_num in range(10):
                    subject_type = SubjectType.objects.create(field_of_study=field_of_study,
                                                              name=f'subject_type{department_num}{field_of_study_num}{subject_type_num}',
                                                              points_to_give=random.randint(6, 10))

                    # lecture
                    Subject.objects.create(subject_type=subject_type,
                                           description=f'description{department_num}{field_of_study_num}{subject_type_num}',
                                           lecturer=f'lecturer{random.randint(0, 10)}',
                                           day='MONDAY',
                                           type='L',
                                           start_time=generate_time(),
                                           end_time=generate_time(),
                                           limit=200)
                    # practice
                    for practice_num in range(8):
                        Subject.objects.create(subject_type=subject_type,
                                               description=f'description{subject_type_num}',
                                               lecturer=f'lecturer{{random.randint(0, 10)}}',
                                               day='MONDAY',
                                               type='P',
                                               start_time=generate_time(),
                                               end_time=generate_time(),
                                               limit=15)

                for student_num in range(100):
                    student_user = djc_auth.get_user_model()(
                        username=f'student{department_num}{field_of_study_num}{student_num}',
                        email=f'student{department_num}{field_of_study_num}{student_num}@gmail.com')
                    student_user.set_password('pass')
                    student_user.save()

                    student = Student.objects.create(field_of_study=field_of_study, user=student_user)

                    subjects_types = SubjectType.objects.filter(field_of_study=field_of_study)

                    for subject_type in subjects_types:
                        students_points_to_give = subject_type.points_to_give
                        practices = Subject.objects.filter(type='P',
                                                           subject_type=subject_type)
                        for (j, subject) in enumerate(practices):
                            if students_points_to_give == 0:
                                break
                            if j == len(practices) - 1:
                                Points(student=student, subject=subject,
                                       points=students_points_to_give).save()
                                break
                            points_given = random.randint(1, students_points_to_give)
                            Points(student=student, subject=subject,
                                   points=points_given).save()
                            students_points_to_give -= points_given
