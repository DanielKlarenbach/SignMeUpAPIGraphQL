import os

from django.test import RequestFactory

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, SubjectType, \
    Subject, Student, SubjectGroup, Application, Points

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

import django.test
import graphene.test
import django.contrib.auth as djc_auth
import graphql_jwt.shortcuts as gql_jwt_shortcuts

from SignMeUpAPIGraphQL.schema import schema


class TestUpdateSchema(django.test.TestCase):
    def setUp(self) -> None:
        super(TestUpdateSchema, self).setUp()
        self.client = graphene.test.Client(schema)

        self.university_admin_user = djc_auth.get_user_model()(username="university_admin",
                                                               email="university_admin@gmail.com")
        self.university_admin_user.set_password('pass')
        self.university_admin_user.save()
        token = gql_jwt_shortcuts.get_token(self.university_admin_user)
        self.university_admin_headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

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

        self.subject_type = SubjectType.objects.create(field_of_study=self.field_of_study, name='subject_type')

        self.subject1 = Subject.objects.create(subject_type=self.subject_type, description='description',
                                               lecturer='ecturer',
                                               day='MONDAY',
                                               type='P',
                                               start_time='14:30',
                                               end_time='16:00',
                                               limit=15)

        self.subject2 = Subject.objects.create(subject_type=self.subject_type, description='description',
                                               lecturer='lecturer',
                                               day='MONDAY',
                                               type='P',
                                               start_time='14:30',
                                               end_time='16:00',
                                               limit=15)

        self.student_user = djc_auth.get_user_model()(username="student",
                                                      email="student@gmail.com")
        self.student_user.set_password('pass')
        self.student_user.save()
        token = gql_jwt_shortcuts.get_token(self.student_user)
        self.student_user_headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        self.student = Student.objects.create(user=self.student_user, field_of_study=self.field_of_study)

    def test_update_user(self):
        mutation = '''
            mutation UpdateUser($username : String!, $email : String!){
                updateUser(username: $username, email : $email){
                    user{
                        username
                    }
                }
            }
        '''
        input = {
            'username': 'updated_university_admin',
            'email': 'updated_university_admin@gmail.com'
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        print(response)
        db_user = djc_auth.get_user_model().objects.get(username=input['username'])
        self.assertEqual(db_user.username, input['username'])
        response_user = response.get("data").get("updateUser").get("user")
        self.assertEqual(response_user['username'], input['username'])
