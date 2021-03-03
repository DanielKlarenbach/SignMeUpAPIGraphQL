import os

from django.test import RequestFactory

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, SubjectType, \
    Subject, Student, Points, SubjectGroup, Application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

import django.test
import graphene.test
import django.contrib.auth as djc_auth
import graphql_jwt.shortcuts as gql_jwt_shortcuts

from SignMeUpAPIGraphQL.schema import schema


class TestDeleteSchema(django.test.TestCase):
    def setUp(self) -> None:
        super(TestDeleteSchema, self).setUp()
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

        self.points = Points.objects.create(student=self.student, subject=self.subject1, points=8)

        self.subject_group = SubjectGroup.objects.create(student=self.student, subject=self.subject1)

        self.application = Application.objects.create(student=self.student, unwanted_subject=self.subject1,
                                                      wanted_subject=self.subject2)

    def test_delete_university_admin(self):
        mutation = '''
            mutation DeleteUniversityAdmin{
                deleteUniversityAdmin{
                    universityAdmin{
                        user{
                            username
                        }
                    }
                }
            }
        '''
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(UniversityAdmin.DoesNotExist):
            UniversityAdmin.objects.get(user=self.university_admin_user)

    def test_delete_department_admin(self):
        mutation = '''
            mutation DeleteDepartmentAdmin($id : Int!){
                deleteDepartmentAdmin(id : $id){
                    departmentAdmin{
                        user{
                            username
                        }
                    }
                }
            }
        '''
        input = {
            'id': self.department_admin.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(DepartmentAdmin.DoesNotExist):
            DepartmentAdmin.objects.get(id=input['id'])

    def test_delete_department(self):
        mutation = '''
            mutation DeleteDepartment($id : Int!){
                deleteDepartment(id : $id){
                    department{
                        name
                    }
                }
            }
        '''
        input = {
            'id': self.department.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.university_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.university_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(Department.DoesNotExist):
            Department.objects.get(id=input['id'])

    def test_delete_year(self):
        mutation = '''
            mutation DeleteYear($id : Int!){
                deleteYear(id : $id){
                    year{
                        startYear
                    }
                }
            }
        '''
        input = {
            'id': self.year.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(Year.DoesNotExist):
            Year.objects.get(id=input['id'])

    def test_delete_field_of_study(self):
        mutation = '''
            mutation DeleteFieldOfStudy($id : Int!){
                deleteFieldOfStudy(id : $id){
                    fieldOfStudy{
                        name
                    }
                }
            }
        '''
        input = {
            'id': self.field_of_study.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(FieldOfStudy.DoesNotExist):
            FieldOfStudy.objects.get(id=input['id'])

    def test_delete_subject(self):
        mutation = '''
            mutation DeleteSubject($id : Int!){
                deleteSubject(id : $id){
                    subject{
                        lecturer
                    }
                }
            }
        '''
        input = {
            'id': self.subject1.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=input['id'])

    def test_delete_student(self):
        mutation = '''
            mutation DeleteStudent($id : Int!){
                deleteStudent(id : $id){
                    student{
                        user{
                            username
                        }
                    }
                }
            }
        '''
        input = {
            'id': self.student.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(id=input['id'])

    def test_delete_subject_group(self):
        mutation = '''
            mutation DeleteSubjectGroup($id : Int!){
                deleteSubjectGroup(id : $id){
                    subjectGroup{
                        student{
                            user{
                                username
                            }
                        }
                    }
                }
            }
        '''
        input = {
            'id': self.subject_group.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.department_admin_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.department_admin_headers,
            context_value=context_value
        )
        with self.assertRaises(SubjectGroup.DoesNotExist):
            SubjectGroup.objects.get(id=input['id'])

    def test_delete_application(self):
        mutation = '''
            mutation DeleteApplication($id : Int!){
                deleteApplication(id : $id){
                    application{
                        student{
                            user{
                                username
                            }
                        }
                    }
                }
            }
        '''
        input = {
            'id': self.application.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.student_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.student_user_headers,
            context_value=context_value
        )
        with self.assertRaises(Application.DoesNotExist):
            Application.objects.get(id=input['id'])

    def test_delete_points(self):
        mutation = '''
            mutation DeletePoints($id : Int!){
                deletePoints(id : $id){
                    points{
                        points
                    }
                }
            }
        '''
        input = {
            'id': self.points.id
        }
        context_value = RequestFactory().get('/api/')
        context_value.user = self.student_user
        response = self.client.execute(
            mutation,
            variables=input,
            headers=self.student_user_headers,
            context_value=context_value
        )
        with self.assertRaises(Points.DoesNotExist):
            Points.objects.get(id=input['id'])
