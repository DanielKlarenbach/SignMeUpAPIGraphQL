import os
import random

from django.test import RequestFactory

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, SubjectType, \
    Subject, Student, Points

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

import django.test
import graphene.test
import django.contrib.auth as djc_auth
import graphql_jwt.shortcuts as gql_jwt_shortcuts

from SignMeUpAPIGraphQL.schema import schema


class TestMakeGroupsSchema(django.test.TestCase):
    def setUp(self) -> None:
        super(TestMakeGroupsSchema, self).setUp()
        self.client = graphene.test.Client(schema)

        self.university_admin_user = djc_auth.get_user_model()(username="university_admin",
                                                               email="university_admin@gmail.com")
        self.university_admin_user.set_password('pass')
        self.university_admin_user.save()

        self.university_admin = UniversityAdmin.objects.create(user=self.university_admin_user)

        self.university = University.objects.create(university_admin=self.university_admin, name='university')

        self.department = Department.objects.create(university=self.university, name='department')

        self.department_admin_user = djc_auth.get_user_model()(username="department_admin",
                                                               email="department_admin@gmail.com")
        self.department_admin_user.set_password('pass')
        self.department_admin_user.save()
        token = gql_jwt_shortcuts.get_token(self.department_admin_user)
        self.department_admin_headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        self.department_admin = DepartmentAdmin.objects.create(user=self.department_admin_user,
                                                               department=self.department)

        self.year = Year.objects.create(start_year=2016, department=self.department)

        self.field_of_study = FieldOfStudy.objects.create(year=self.year, name='field_of_study')

        for i in range(10):
            SubjectType.objects.create(field_of_study=self.field_of_study, name=f'subject_type{i}', points_to_give=8)

        for (i, subject_type) in enumerate(SubjectType.objects.filter(field_of_study=self.field_of_study)):
            Subject.objects.create(subject_type=subject_type, description=f'description{i}',
                                   lecturer=f'lecturer{i}',
                                   day='MONDAY',
                                   type='L',
                                   start_time='14:30',
                                   end_time='16:00',
                                   limit=100)
            for j in range(4):
                Subject.objects.create(subject_type=subject_type, description=f'description{j}',
                                       lecturer=f'lecturer{j}',
                                       day='MONDAY',
                                       type='P',
                                       start_time='14:30',
                                       end_time='16:00',
                                       limit=100)

        for i in range(30):
            student_user = djc_auth.get_user_model()(username=f'student{i}',
                                                     email=f'student{i}@gmail.com')
            student_user.set_password('pass')
            student_user.save()
            student = Student.objects.create(field_of_study=self.field_of_study, user=student_user)

            subjects_types = SubjectType.objects.filter(field_of_study=self.field_of_study)

            for subject_type in subjects_types:
                students_points_to_give = subject_type.points_to_give
                practices = Subject.objects.filter(field_of_study=self.field_of_study, type='P',
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

    def test_make_groups(self):
        mutation = '''
            mutation MakeGroups($fieldOfStudyId : Int!){
                makeGroups(fieldOfStudyId : $fieldOfStudyId){
                    ok
                }
            }
        '''
        input = {
            'fieldOfStudyId': self.field_of_study,
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
