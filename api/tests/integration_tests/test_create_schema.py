import os

from django.test import RequestFactory

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, SubjectType, \
    Subject, Student

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

import django.test
import graphene.test
import django.contrib.auth as djc_auth
import graphql_jwt.shortcuts as gql_jwt_shortcuts

from SignMeUpAPIGraphQL.schema import schema


class TestCreateSchema(django.test.TestCase):
    def setUp(self) -> None:
        super(TestCreateSchema, self).setUp()
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

        self.student_user=djc_auth.get_user_model()(username="student",
                                                               email="student@gmail.com")
        self.student_user.set_password('pass')
        self.student_user.save()
        token = gql_jwt_shortcuts.get_token(self.student_user)
        self.student_user_headers = {"HTTP_AUTHORIZATION": f"JWT {token}"}

        self.student=Student.objects.create(user=self.student_user,field_of_study=self.field_of_study)

    def test_create_university(self):
        mutation = '''
            mutation CreateUniversityAdmin($universityName: String!, $username : String!, $password : String!, $email : String!){
                createUniversityAdmin(universityName: $universityName, username: $username, password: $password, email : $email){
                    ok
                }
            }
        '''
        input = {
            'universityName': 'test_university',
            'username': 'test_university_admin',
            'password': 'pass',
            'email': 'test_university_admin@gmail.com'
        }
        response = self.client.execute(
            mutation,
            variables=input,
        )
        print(response)
        ok = response.get("data").get("createUniversityAdmin").get("ok")
        self.assertTrue(ok)

    def test_create_department(self):
        mutation = '''
            mutation CreateDepartment($name : String!){
                createDepartment(name: $name){
                    ok
                }
            }
        '''
        input = {
            'name': 'test_department',
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
        ok = response.get("data").get("createDepartment").get("ok")
        self.assertTrue(ok)

    def test_create_department_admin(self):
        mutation = '''
            mutation CreateDepartmentAdmin($departmentId: Int!, $username : String!, $password : String!, $email : String!){
                createDepartmentAdmin(departmentId: $departmentId, username: $username, password: $password, email : $email){
                    ok
                }
            }
        '''
        input = {
            'departmentId': self.department.id,
            'username': 'test_department_admin',
            'password': 'pass',
            'email': 'test_department_admin@gmail.com'
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
        ok = response.get("data").get("createDepartmentAdmin").get("ok")
        self.assertTrue(ok)

    def test_create_year(self):
        mutation = '''
            mutation CreateYear($startYear: Int!){
                createYear(startYear: $startYear){
                    ok
                }
            }
        '''
        input = {
            'startYear': 2017
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createYear").get("ok")
        self.assertTrue(ok)

    def test_create_field_of_study(self):
        mutation = '''
            mutation CreateFieldOfStudy($yearId: Int!,$name : String!){
                createFieldOfStudy(yearId: $yearId,name : $name){
                    ok
                }
            }
        '''
        input = {
            'yearId': self.year.id,
            'name': 'test_field_of_study'
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createFieldOfStudy").get("ok")
        self.assertTrue(ok)

    def test_create_subject_type(self):
        mutation = '''
            mutation CreateSubjectType($fieldOfStudyId: Int!,$name : String!){
                createSubjectType(fieldOfStudyId: $fieldOfStudyId,name : $name){
                    ok
                }
            }
        '''
        input = {
            'fieldOfStudyId': self.field_of_study.id,
            'name': 'test_subject_type'
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createSubjectType").get("ok")
        self.assertTrue(ok)

    def test_create_subject(self):
        mutation = '''
            mutation CreateSubject($subjectTypeId: Int!,$description : String!, $lecturer: String!, $day : String!, $type : String!, $startTime : Time!, $endTime : Time!, $limit : Int!){
                createSubject(subjectTypeId: $subjectTypeId,description : $description, lecturer : $lecturer, day : $day, type : $type, startTime : $startTime, endTime : $endTime, limit : $limit){
                    ok
                }
            }
        '''
        input = {
            'subjectTypeId': self.subject_type.id,
            'description': 'test_description',
            'lecturer': 'test_lecturer',
            'day': 'MONDAY',
            'type': 'P',
            'startTime': '14:30',
            'endTime': '16:00',
            'limit': 15
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createSubject").get("ok")
        self.assertTrue(ok)

    def test_create_student(self):
        mutation = '''
            mutation CreateStudent($fieldOfStudyId: Int!, $username : String!, $password : String!, $email : String!){
                createStudent(fieldOfStudyId: $fieldOfStudyId, username: $username, password: $password, email : $email){
                    ok
                }
            }
        '''
        input = {
            'fieldOfStudyId': self.field_of_study.id,
            'username': 'test_student',
            'password': 'pass',
            'email': 'test_student@gmail.com'
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createStudent").get("ok")
        self.assertTrue(ok)

    def test_create_subject_group(self):
        mutation = '''
            mutation CreateSubjectGroup($subjectId: Int!, $studentId : Int!){
                createSubjectGroup(subjectId: $subjectId, studentId: $studentId){
                    ok
                }
            }
        '''
        input = {
            'subjectId' : self.subject1.id,
            'studentId' : self.student.id
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createSubjectGroup").get("ok")
        self.assertTrue(ok)

    def test_create_applications(self):
        mutation = '''
            mutation CreateApplication($unwantedSubjectId: Int!, $wantedSubjectId : Int!, $studentId : Int!){
                createApplication(unwantedSubjectId: $unwantedSubjectId, wantedSubjectId : $wantedSubjectId, studentId: $studentId){
                    ok
                }
            }
        '''
        input = {
            'unwantedSubjectId' : self.subject1.id,
            'wantedSubjectId': self.subject2.id,
            'studentId' : self.student.id
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.student_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.student_user_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get('createApplication').get("ok")
        self.assertTrue(ok)

    def test_create_points(self):
        mutation = '''
            mutation CreatePoints($subjectId: Int!, $studentId : Int!, $points : Int!){
                createPoints(subjectId: $subjectId, studentId: $studentId, points : $points){
                    ok
                }
            }
        '''
        input = {
            'subjectId' : self.subject1.id,
            'studentId' : self.student.id,
            'points' : 8
        }

        context_value = RequestFactory().get('/api/')
        context_value.user = self.student_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.student_user_headers,
            context_value=context_value
        )
        print(response)
        ok = response.get("data").get("createPoints").get("ok")
        self.assertTrue(ok)

