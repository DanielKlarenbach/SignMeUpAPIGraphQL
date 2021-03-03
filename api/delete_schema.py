import graphene

from api.models import DepartmentAdmin, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, \
    Application, Points, UniversityAdmin
from api.permissions import is_logged_in, is_objects_university_admin, is_owner, is_objects_department_admin, \
    is_university_admin
from api.retrieve_schema import DepartmentNode, YearNode, FieldOfStudyNode, SubjectNode, \
    StudentNode, SubjectGroupNode, ApplicationNode, PointsNode, UniversityAdminNode, DepartmentAdminNode


class DeleteUniversityAdmin(graphene.Mutation):
    university_admin = graphene.Field(UniversityAdminNode)

    @classmethod
    @is_logged_in()
    @is_university_admin()
    def mutate(cls, root, info):
        university_admin_user = info.context.user
        university_admin = UniversityAdmin.objects.get(user=university_admin_user)
        university_admin_user.delete()
        return DeleteUniversityAdmin(university_admin=university_admin)


class DeleteDepartmentAdmin(graphene.Mutation):
    department_admin = graphene.Field(DepartmentAdminNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_university_admin(model=DepartmentAdmin, lookup='department__university__university_admin')
    def mutate(cls, root, info, id):
        department_admin = DepartmentAdmin.objects.get(id=id)
        department_admin.user.delete()
        return DeleteDepartmentAdmin(department_admin=department_admin)


class DeleteDepartment(graphene.Mutation):
    department = graphene.Field(DepartmentNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_university_admin(model=Department)
    def mutate(cls, root, info, id):
        department = Department.objects.get(id=id)
        department.delete()
        return DeleteDepartment(department=department)


class DeleteYear(graphene.Mutation):
    year = graphene.Field(YearNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Year)
    def mutate(cls, root, info, id):
        year = Year.objects.get(id=id)
        year.delete()
        return DeleteYear(year=year)


class DeleteFieldOfStudy(graphene.Mutation):
    field_of_study = graphene.Field(FieldOfStudyNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department')
    def mutate(cls, root, info, id):
        field_of_study = FieldOfStudy.objects.get(id=id)
        field_of_study.delete()
        return DeleteFieldOfStudy(field_of_study=field_of_study)


class DeleteSubject(graphene.Mutation):
    subject = graphene.Field(SubjectNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Subject, lookup='subject_type__field_of_study__year__department')
    def mutate(cls, root, info, id):
        subject = Subject.objects.get(id=id)
        subject.delete()
        return DeleteSubject(subject=subject)


class DeleteStudent(graphene.Mutation):
    student = graphene.Field(StudentNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Student, lookup='field_of_study__year__department')
    def mutate(cls, root, info, id):
        student = Student.objects.get(id=id)
        student.delete()
        return DeleteStudent(student=student)


class DeleteSubjectGroup(graphene.Mutation):
    subject_group = graphene.Field(SubjectGroupNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=SubjectGroup, lookup='subject__subject_type__field_of_study__year__department')
    def mutate(cls, root, info, id):
        subject_group = SubjectGroup.objects.get(id=id)
        subject_group.delete()
        return DeleteSubjectGroup(subject_group=subject_group)


class DeleteApplication(graphene.Mutation):
    application = graphene.Field(ApplicationNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Application, lookup='student__user')
    def mutate(cls, root, info, id):
        application = Application.objects.get(id=id)
        application.delete()
        return DeleteApplication(application=application)


class DeletePoints(graphene.Mutation):
    points = graphene.Field(PointsNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Points, lookup='student__user')
    def mutate(cls, root, info, id):
        points = Points.objects.get(id=id)
        points.delete()
        return DeletePoints(points=points)


class Mutation(graphene.ObjectType):
    delete_university_admin = DeleteUniversityAdmin.Field()
    delete_department_admin = DeleteDepartmentAdmin.Field()
    delete_department = DeleteDepartment.Field()
    delete_year = DeleteYear.Field()
    delete_field_of_study = DeleteFieldOfStudy.Field()
    delete_subject = DeleteSubject.Field()
    delete_student = DeleteStudent.Field()
    delete_subject_group = DeleteSubjectGroup.Field()
    delete_points = DeletePoints.Field()
    delete_application = DeleteApplication.Field()
