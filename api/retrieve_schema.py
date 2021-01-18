import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType


from api.models import University, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, Points, Application, \
    UniversityAdmin, DepartmentAdmin


class UserNode(DjangoObjectType):
    class Meta:
        model = get_user_model()
        fields = ('university_admin','department_admin','students','username')

class UniversityAdminNode(DjangoObjectType):

    class Meta:
        model=UniversityAdmin
        fields = ('user','university','departments','department_admins')

class DepartmentAdminNode(DjangoObjectType):
    class Meta:
        model=DepartmentAdmin
        fields = ('user','department')

class UniversityNode(DjangoObjectType):

    class Meta:
        model=University
        fields = ('name',)

class DepartmentNode(DjangoObjectType):

    class Meta:
        model=Department
        fields = ('id','name','university')

class YearNode(DjangoObjectType):

    class Meta:
        model=Year
        fields = ('department','start_year','fields_of_study')

class FieldOfStudyNode(DjangoObjectType):

    class Meta:
        model=FieldOfStudy
        fields =('name','subjects','students')

class SubjectNode(DjangoObjectType):

    class Meta:
        model=Subject
        fields=('name','description','lecturer','type','day','start_time','end_time')

class StudentNode(DjangoObjectType):

    class Meta:
        model = Student
        fields=('user','points','applications')

class SubjectGroupNode(DjangoObjectType):

    class Meta:
        model=SubjectGroup
        fields=('subject','student')

class PointsNode(DjangoObjectType):

    class Meta:
        model=Points
        fields=('subject','points')

class ApplicationNode(DjangoObjectType):

    class Meta:
        model=Application
        fields=('unwanted_subject','wanted_subject','priority','created_at')

class Query(graphene.ObjectType):
    subject_groups_by_student = graphene.Field(SubjectGroupNode, student_id=graphene.Int(required=True))
    subject_groups_by_subject = graphene.Field(SubjectNode, subject_id=graphene.Int(required=True))
    years_by_department = graphene.Field(YearNode)
    #year_by_student =
    me = graphene.Field(UserNode)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in')
        return user

    def resolve_subject_groups_by_student(root, info,student_id,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to browse through your groups')
        student=Student.objects.get(user=user,id=student_id)
        if student is None:
            raise Exception('You are not authorized to browse through this students groups')
        return SubjectGroup.objects.filter(student=student)

    def resolve_subject_groups_by_subject(root, info,subject_id,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to browse through subjects group')
        department_admin=DepartmentAdmin.objects.get(user=user)
        if department_admin is None:
            raise Exception('You are not authorized to browse through this subjects group. You are not a department admin')
        subject = Subject.objects.get(field_of_study__year__department=department_admin.department,id=subject_id)
        if subject is None:
            raise Exception('You are not authorized to browse through this subjects group. This subject is outside of your department')
        return SubjectGroup.objects.filter(subject=subject)

    def resolve_years_by_department(root, info,**kwargs):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to browse through departments years')
        department_admin=DepartmentAdmin.objects.get(user=user)
        if department_admin is None:
            raise Exception('You are not authorized to browse through departments years. You are not a department admin')
        return Year.objects.get(department_admin=department_admin)



