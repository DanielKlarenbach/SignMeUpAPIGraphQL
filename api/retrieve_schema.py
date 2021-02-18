import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from api.models import University, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application, \
    UniversityAdmin, DepartmentAdmin
from api.permissions import is_logged_in, is_objects_university_admin, is_department_admin


class SubjectGroupNode(DjangoObjectType):
    class Meta:
        model = SubjectGroup
        fields = ('id', 'subject', 'student')


class PointsNode(DjangoObjectType):
    class Meta:
        model = Points
        fields = ('id', 'points', 'subject', 'student')


class ApplicationNode(DjangoObjectType):
    class Meta:
        model = Application
        fields = ('id', 'priority', 'created_at', 'unwanted_subject', 'wanted_subject', 'student')


class SubjectNode(DjangoObjectType):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'lecturer', 'type', 'day', 'start_time', 'end_time', 'field_of_study')

    subject_groups = graphene.List(SubjectGroupNode)
    points = graphene.List(PointsNode)
    applications = graphene.List(ApplicationNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_subject_groups(self, info):
        return SubjectGroup.objects.get(subject=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_points(self, info):
        return Points.objects.get(subject=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_applications(self, info):
        return Application.objects.get(subject=self)


class StudentNode(DjangoObjectType):
    class Meta:
        model = Student
        fields = ('id', 'user', 'points', 'applications', 'subject_groups', 'field_of_study')


class FieldOfStudyNode(DjangoObjectType):
    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'subjects')

    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.get(field_of_study=self)


class YearNode(DjangoObjectType):
    class Meta:
        model = Year
        fields = ('id', 'department', 'start_year')

    fields_of_study = graphene.List(FieldOfStudyNode)
    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_fields_of_study(self, info):
        return FieldOfStudy.objects.get(year=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.get(field_of_study__year=self)


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        fields = ('id', 'name', 'university', 'department_admins')

    years = graphene.List(YearNode)
    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_years(self, info):
        return Year.objects.get(department=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.get(field_of_study__year__department=self)


class DepartmentAdminNode(DjangoObjectType):
    class Meta:
        model = DepartmentAdmin
        fields = ('id', 'user', 'department')


class UniversityNode(DjangoObjectType):
    class Meta:
        model = University
        fields = ('id', 'name', 'university_admin')

    departments = graphene.List(DepartmentNode)
    department_admins = graphene.List(DepartmentAdminNode)

    @is_logged_in(info_index=1)
    @is_objects_university_admin(model=University, info_index=1)
    def resolve_departments(self, info):
        return Department.objects.get(university=self)

    @is_logged_in(info_index=1)
    @is_objects_university_admin(model=University, info_index=1)
    def resolve_department_admins(self, info):
        return DepartmentAdmin.objects.get(department__university=self)


class UniversityAdminNode(DjangoObjectType):
    class Meta:
        model = UniversityAdmin
        fields = ('id', 'user', 'university')


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'students', 'department_admin', 'university_admin')


class Query(graphene.ObjectType):
    me = graphene.Field(UserNode)

    @is_logged_in(info_index=1)
    def resolve_me(self, info):
        user = info.context.user
        return user
