import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from api.models import University, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application, \
    UniversityAdmin, DepartmentAdmin, SubjectType
from api.permissions import is_logged_in, is_department_admin, is_university_admin


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
        fields = ('id', 'created_at', 'unwanted_subject', 'wanted_subject', 'student')


class SubjectNode(DjangoObjectType):
    class Meta:
        model = Subject
        fields = (
            'id', 'description', 'lecturer', 'type', 'day', 'start_time', 'end_time', 'limit', 'subject_type')

    subject_groups = graphene.List(SubjectGroupNode)
    points = graphene.List(PointsNode)
    applications = graphene.List(ApplicationNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_subject_groups(self, info):
        return SubjectGroup.objects.filter(subject=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_points(self, info):
        return Points.objects.filter(subject=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_applications(self, info):
        return Application.objects.filter(subject=self)


class SubjectTypeNode(DjangoObjectType):
    class Meta:
        model = SubjectType
        fields = ('id', 'name', 'subjects')


class StudentNode(DjangoObjectType):
    class Meta:
        model = Student
        fields = ('id', 'user', 'points', 'applications', 'subject_groups', 'field_of_study')


class FieldOfStudyNode(DjangoObjectType):
    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'year', 'subject_types')

    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.filter(field_of_study=self)


class YearNode(DjangoObjectType):
    class Meta:
        model = Year
        fields = ('id', 'department', 'start_year')

    fields_of_study = graphene.List(FieldOfStudyNode)
    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_fields_of_study(self, info):
        return FieldOfStudy.objects.filter(year=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.filter(field_of_study__year=self)


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        fields = ('id', 'name', 'university', 'department_admins')

    years = graphene.List(YearNode)
    students = graphene.List(StudentNode)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_years(self, info):
        return Year.objects.filter(department=self)

    @is_logged_in(info_index=1)
    @is_department_admin(info_index=1)
    def resolve_students(self, info):
        return Student.objects.filter(field_of_study__year__department=self)


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
    @is_university_admin(info_index=1)
    def resolve_departments(self, info):
        print(Department.objects.filter(university=self))
        return Department.objects.filter(university=self)

    @is_logged_in(info_index=1)
    @is_university_admin(info_index=1)
    def resolve_department_admins(self, info):
        return DepartmentAdmin.objects.filter(department__university=self)


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
