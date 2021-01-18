import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType

from api.models import University, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application, \
    UniversityAdmin, DepartmentAdmin
from api.permissions import is_logged_in, is_owner, is_objects_department_admin, is_department_admin


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('university_admin', 'department_admin', 'students', 'username', 'email')


class UniversityAdminNode(DjangoObjectType):
    class Meta:
        model = UniversityAdmin
        fields = ('id', 'user', 'university', 'departments', 'department_admins')


class DepartmentAdminNode(DjangoObjectType):
    class Meta:
        model = DepartmentAdmin
        fields = ('id', 'user', 'department')


class UniversityNode(DjangoObjectType):
    class Meta:
        model = University
        fields = ('id', 'name',)


class DepartmentNode(DjangoObjectType):
    class Meta:
        model = Department
        fields = ('id', 'name', 'university')


class YearNode(DjangoObjectType):
    class Meta:
        model = Year
        fields = ('id', 'department', 'start_year', 'fields_of_study')


class FieldOfStudyNode(DjangoObjectType):
    class Meta:
        model = FieldOfStudy
        fields = ('id', 'name', 'subjects', 'students')


class SubjectNode(DjangoObjectType):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'description', 'lecturer', 'type', 'day', 'start_time', 'end_time')


class StudentNode(DjangoObjectType):
    class Meta:
        model = Student
        fields = ('id', 'user', 'points', 'applications')


class SubjectGroupNode(DjangoObjectType):
    class Meta:
        model = SubjectGroup
        fields = ('id', 'subject', 'student')


class PointsNode(DjangoObjectType):
    class Meta:
        model = Points
        fields = ('id', 'subject', 'points')


class ApplicationNode(DjangoObjectType):
    class Meta:
        model = Application
        fields = ('id', 'unwanted_subject', 'wanted_subject', 'priority', 'created_at')


class Query(graphene.ObjectType):
    subject_groups_by_student = graphene.Field(SubjectGroupNode, student_id=graphene.Int(required=True))
    subject_groups_by_subject = graphene.Field(SubjectNode, subject_id=graphene.Int(required=True))
    years_by_department = graphene.Field(YearNode)
    me = graphene.Field(UserNode)

    @is_logged_in(info_index=1)
    def resolve_me(self, info):
        user = info.context.user
        return user

    @is_logged_in(info_index=1)
    @is_owner(model=Student, id_kwarg='student_id')
    def resolve_subject_groups_by_student(root, info, student_id):
        return SubjectGroup.objects.filter(student_id=student_id)

    @is_logged_in(info_index=1)
    @is_objects_department_admin(model=Subject, lookup='field_of_study__year__department', id_kwarg='subject_id')
    def resolve_subject_groups_by_subject(root, info, subject_id, **kwargs):
        return SubjectGroup.objects.filter(subject_id=subject_id)

    @is_logged_in(info_index=1)
    @is_department_admin
    def resolve_years_by_department(root, info, **kwargs):
        user = info.context.user
        return Year.objects.get(department_admin=user.department_admin)
