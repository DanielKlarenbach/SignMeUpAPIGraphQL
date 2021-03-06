import graphene
from django.contrib.auth import get_user_model
from django.db import transaction

from api.models import UniversityAdmin, University, Department, DepartmentAdmin, Year, FieldOfStudy, Subject, Student, \
    SubjectGroup, Points, Application, SubjectType
from api.permissions import is_logged_in, is_department_admin, is_university_admin, is_objects_university_admin, \
    is_objects_department_admin, is_owner
from api.retrieve_schema import DepartmentNode, UniversityAdminNode, YearNode, \
    FieldOfStudyNode, \
    SubjectNode, StudentNode, SubjectGroupNode, DepartmentAdminNode, PointsNode, ApplicationNode, SubjectTypeNode
from api.tasks import check_for_matching_application


class CreateUniversityAdmin(graphene.Mutation):
    university_admin = graphene.Field(UniversityAdminNode)

    class Arguments:
        university_name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @classmethod
    @transaction.atomic
    def mutate(cls, root, info, university_name, username, password, email):
        university_admin_user = get_user_model()(username=username, email=email)
        university_admin_user.set_password(password)
        university_admin_user.save()
        university_admin = UniversityAdmin.objects.create(user=university_admin_user)
        University(name=university_name, university_admin=university_admin).save()
        return CreateUniversityAdmin(university_admin=university_admin)


class CreateDepartment(graphene.Mutation):
    department = graphene.Field(DepartmentNode)

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_university_admin()
    def mutate(cls, root, info, name):
        university_admin_user = info.context.user
        university = university_admin_user.university_admin.university
        department = Department.objects.create(university=university, name=name)
        return CreateDepartment(department=department)


class CreateDepartmentAdmin(graphene.Mutation):
    department_admin = graphene.Field(DepartmentAdminNode)

    class Arguments:
        department_id = graphene.Int(required=True, name='departmentId')
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @classmethod
    @transaction.atomic
    @is_logged_in()
    @is_objects_university_admin(model=Department, id_kwarg='department_id')
    def mutate(cls, root, info, department_id, username, password, email):
        department_admin_user = get_user_model()(username=username, email=email)
        department_admin_user.set_password(password)
        department_admin_user.save()
        department_admin = DepartmentAdmin.objects.create(user=department_admin_user,
                                                          department_id=department_id)
        return CreateDepartmentAdmin(department_admin=department_admin)


class CreateYear(graphene.Mutation):
    year = graphene.Field(YearNode)

    class Arguments:
        start_year = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_department_admin()
    def mutate(cls, root, info, start_year):
        department_admin_user = info.context.user
        department = department_admin_user.department_admin.department
        year = Year.objects.create(start_year=start_year, department=department)
        return CreateYear(year=year)


class CreateFieldOfStudy(graphene.Mutation):
    field_of_study = graphene.Field(FieldOfStudyNode)

    class Arguments:
        year_id = graphene.Int(required=True, name="yearId")
        name = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Year, id_kwarg='year_id')
    def mutate(cls, root, info, year_id, name):
        field_of_study = FieldOfStudy.objects.create(name=name, year_id=year_id)
        return CreateFieldOfStudy(field_of_study=field_of_study)


class CreateSubjectType(graphene.Mutation):
    subject_type = graphene.Field(SubjectTypeNode)

    class Arguments:
        field_of_study_id = graphene.Int(required=True, name='fieldOfStudyId')
        name = graphene.String(required=True)
        points_to_give = graphene.Int(required=True, name='pointsToGive')

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department', id_kwarg='field_of_study_id')
    def mutate(cls, root, info, field_of_study_id, name, points_to_give):
        subject_type = SubjectType.objects.create(field_of_study_id=field_of_study_id, name=name,
                                                  points_to_give=points_to_give)
        return CreateSubjectType(subject_type=subject_type)


class CreateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectNode)

    class Arguments:
        subject_type_id = graphene.Int(required=True, name='subjectTypeId')
        description = graphene.String(required=True)
        lecturer = graphene.String(required=True)
        day = graphene.String(required=True)
        type = graphene.String(required=True)
        start_time = graphene.Time(required=True)
        end_time = graphene.Time(required=True)
        limit = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=SubjectType, lookup='field_of_study__year__department',
                                 id_kwarg='subject_type_id')
    def mutate(cls, root, info, subject_type_id, description, lecturer, day, type, start_time, end_time, limit):
        subject = Subject.objects.create(subject_type_id=subject_type_id, description=description,
                                         lecturer=lecturer, day=day, type=type, start_time=start_time,
                                         end_time=end_time, limit=limit)
        return CreateSubject(subject=subject)


class CreateStudent(graphene.Mutation):
    student = graphene.Field(StudentNode)

    class Arguments:
        field_of_study_id = graphene.Int(required=True, name='fieldOfStudyId')
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @classmethod
    @transaction.atomic
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department', id_kwarg='field_of_study_id')
    def mutate(cls, root, info, field_of_study_id, username, password, email):
        student_user = get_user_model()(username=username, email=email)
        student_user.set_password(password)
        student_user.save()
        student = Student.objects.create(user=student_user, field_of_study_id=field_of_study_id)
        return CreateStudent(student=student)


class CreateSubjectGroup(graphene.Mutation):
    subject_group = graphene.Field(SubjectGroupNode)

    class Arguments:
        subject_id = graphene.Int(required=True)
        student_id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Student, lookup='field_of_study__year__department', id_kwarg='student_id')
    @is_objects_department_admin(model=Subject, lookup='subject_type__field_of_study__year__department',
                                 id_kwarg='subject_id')
    def mutate(cls, root, info, subject_id, student_id):
        subject_group = SubjectGroup.objects.create(subject_id=subject_id, student_id=student_id)
        subject=Subject.objects.get(id=subject_id)
        subject.occupancy+=1
        subject.save()
        return CreateSubjectGroup(subject_group=subject_group)


class CreatePoints(graphene.Mutation):
    points = graphene.Field(PointsNode)

    class Arguments:
        subject_id = graphene.Int(required=True)
        student_id = graphene.Int(required=True)
        points = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Subject, lookup='subject_type__field_of_study__students__user', id_kwarg='subject_id')
    @is_owner(model=Student, id_kwarg='student_id')
    def mutate(cls, root, info, subject_id, student_id, points):
        points = Points.objects.create(subject_id=subject_id, student_id=student_id, points=points)
        return CreatePoints(points=points)


class CreateApplication(graphene.Mutation):
    application = graphene.Field(ApplicationNode)

    class Arguments:
        unwanted_subject_id = graphene.Int(required=True)
        wanted_subject_id = graphene.Int(required=True)
        student_id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Subject, lookup='subject_type__field_of_study__students__user', id_kwarg='unwanted_subject_id')
    @is_owner(model=Subject, lookup='subject_type__field_of_study__students__user', id_kwarg='wanted_subject_id')
    @is_owner(model=Student, id_kwarg='student_id')
    def mutate(cls, root, info, unwanted_subject_id, wanted_subject_id, student_id):
        application = Application.objects.create(unwanted_subject_id=unwanted_subject_id,
                                                 wanted_subject_id=wanted_subject_id,
                                                 student_id=student_id)
        check_for_matching_application.delay(application.id)
        return CreateApplication(application=application)


class Mutation(graphene.ObjectType):
    create_university_admin = CreateUniversityAdmin.Field()
    create_department = CreateDepartment.Field()
    create_department_admin = CreateDepartmentAdmin.Field()
    create_year = CreateYear.Field()
    create_field_of_study = CreateFieldOfStudy.Field()
    create_student = CreateStudent.Field()
    create_subject_type = CreateSubjectType.Field()
    create_subject = CreateSubject.Field()
    create_points = CreatePoints.Field()
    create_subject_group = CreateSubjectGroup.Field()
    create_application = CreateApplication.Field()
