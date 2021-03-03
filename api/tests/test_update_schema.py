import os

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

        self.subject_type = SubjectType.objects.create(field_of_study=self.field_of_study, name='subject_type',
                                                       points_to_give=8)

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

        self.points = Points.objects.create(student=self.student, subject=self.subject1, points=8)

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
        db_user = djc_auth.get_user_model().objects.get(username=input['username'])
        self.assertEqual(db_user.username, input['username'])
        response_user = response.get("data").get("updateUser").get("user")
        self.assertEqual(response_user['username'], input['username'])

    def test_update_university(self):
        mutation = '''
            mutation UpdateUniversity($name : String!){
                updateUniversity(name : $name){
                    university{
                        name
                    }
                }
            }
        '''
        input = {
            'name': 'updated_university',
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        db_university = University.objects.get(name=input['name'])
        self.assertEqual(db_university.name, input['name'])
        response_university = response.get("data").get("updateUniversity").get("university")
        self.assertEqual(response_university['name'], input['name'])

    def test_update_department(self):
        mutation = '''
            mutation UpdateDepartment($id : Int!, $name : String!){
                updateDepartment(id : $id, name : $name){
                    department{
                        name
                    }
                }
            }
        '''
        input = {
            'id': self.department.id,
            'name': 'updated_department',
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        db_department = Department.objects.get(id=input['id'])
        self.assertEqual(db_department.name, input['name'])
        response_department = response.get("data").get("updateDepartment").get("department")
        self.assertEqual(response_department['name'], input['name'])

    def test_update_year(self):
        mutation = '''
            mutation UpdateYear($id : Int!, $startYear : Int!){
                updateYear(id : $id, startYear : $startYear){
                    year{
                        startYear
                    }
                }
            }
        '''
        input = {
            'id': self.year.id,
            'startYear': 2020,
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        db_year = Year.objects.get(id=input['id'])
        self.assertEqual(db_year.start_year, input['startYear'])
        response_year = response.get("data").get("updateYear").get("year")
        self.assertEqual(response_year['startYear'], input['startYear'])

    def test_update_field_of_study(self):
        mutation = '''
            mutation UpdateFieldOfStudy($id : Int!, $name : String!){
                updateFieldOfStudy(id : $id, name : $name){
                    fieldOfStudy{
                        name
                    }
                }
            }
        '''
        input = {
            'id': self.field_of_study.id,
            'name': 'updated_field_of-study',
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        db_field_of_study = FieldOfStudy.objects.get(id=input['id'])
        self.assertEqual(db_field_of_study.name, input['name'])
        response_field_of_study = response.get("data").get("updateFieldOfStudy").get("fieldOfStudy")
        self.assertEqual(response_field_of_study['name'], input['name'])

    def test_update_subject(self):
        mutation = '''
            mutation UpdateSubject($id : Int!, $lecturer : String!, $limit : Int!){
                updateSubject(id : $id, lecturer : $lecturer, limit : $limit ){
                    subject{
                        limit
                    }
                }
            }
        '''
        input = {
            'id': self.subject1.id,
            'lecturer': 'updated_lecturer',
            'limit': 17,
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        db_subject = Subject.objects.get(id=input['id'])
        self.assertEqual(db_subject.limit, input['limit'])
        response_subject = response.get("data").get("updateSubject").get("subject")
        self.assertEqual(response_subject['limit'], input['limit'])

    def test_update_points(self):
        mutation = '''
            mutation UpdatePoints($id : Int!, $points : Int!){
                updatePoints(id : $id, points : $points){
                    points{
                        points
                    }
                }
            }
        '''
        input = {
            'id': self.points.id,
            'points': 4,
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.student_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.student_user_headers,
            context_value=context_value
        )
        db_points = Points.objects.get(id=input['id'])
        self.assertEqual(db_points.points, input['points'])
        response_points = response.get("data").get("updatePoints").get("points")
        self.assertEqual(response_points['points'], input['points'])
