import graphene

from api.models import DepartmentAdmin, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, \
    Application, Points
from api.permissions import is_logged_in, is_objects_university_admin, is_owner, is_objects_department_admin, \
    is_university_admin
from api.retrieve_schema import DepartmentNode, YearNode, FieldOfStudyNode, SubjectNode, \
    StudentNode, SubjectGroupNode, ApplicationNode, PointsNode, UniversityAdminNode, DepartmentAdminNode


class DeleteUniversityAdmin(graphene.Mutation):
    ok = graphene.Boolean()
    university_admin = graphene.Field(UniversityAdminNode)

    @classmethod
    @is_logged_in()
    @is_university_admin()
    def mutate(cls, root, info):
        university_admin_user = info.context.user
        university_admin = university_admin_user.delete()
        return DeleteDepartmentAdmin(ok=True, university_admin=university_admin)


class DeleteDepartmentAdmin(graphene.Mutation):
    ok = graphene.Boolean()
    department_admin = graphene.Field(DepartmentAdminNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_university_admin(model=DepartmentAdmin)
    def mutate(cls, root, info, id):
        department_admin = DepartmentAdmin.objects.get(id=id).user.delete()
        return DeleteDepartmentAdmin(ok=True, department_admin=department_admin)


class DeleteDepartment(graphene.Mutation):
    ok = graphene.Boolean()
    department = graphene.Field(DepartmentNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_university_admin(model=Department)
    def mutate(cls, root, info, id):
        department = Department.objects.get(id=id).delete()
        return DeleteDepartment(ok=True, department=department)


class DeleteYear(graphene.Mutation):
    ok = graphene.Boolean()
    year = graphene.Field(YearNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Year)
    def mutate(cls, root, info, id):
        year = Year.objects.get(id=id).delete()
        return DeleteYear(ok=True, year=year)


class DeleteFieldOfStudy(graphene.Mutation):
    ok = graphene.Boolean()
    field_of_study = graphene.Field(FieldOfStudyNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department')
    def mutate(cls, root, info, id):
        field_of_study = FieldOfStudy.objects.get(id=id).delete()
        return DeleteFieldOfStudy(ok=True, field_of_study=field_of_study)


class DeleteSubject(graphene.Mutation):
    ok = graphene.Boolean()
    subject = graphene.Field(SubjectNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Subject, lookup='field_of_study__year__department')
    def mutate(cls, root, info, id):
        subject = Subject.objects.get(id=id).delete()
        return DeleteSubject(ok=True, subject=subject)


class DeleteStudent(graphene.Mutation):
    ok = graphene.Boolean()
    student = graphene.Field(StudentNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Student, lookup='field_of_study__year__department')
    def mutate(cls, root, info, id):
        student = Student.objects.get(id=id).delete()
        return DeleteStudent(ok=True, student=student)


class DeleteSubjectGroup(graphene.Mutation):
    ok = graphene.Boolean()
    subject_group = graphene.Field(SubjectGroupNode)

    class Arguments:
        id = graphene.Int(required=True)
        student_id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Student, lookup='field_of_study__year__department', id_kwarg='student_id')
    def mutate(cls, root, info, id, student_id):
        subject_group = SubjectGroup.objects.get(id=id).delete()
        return DeleteSubjectGroup(ok=True, subject_group=subject_group)


class DeleteApplication(graphene.Mutation):
    ok = graphene.Boolean()
    application = graphene.Field(ApplicationNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Application)
    def mutate(cls, root, info, id):
        application = Application.objects.get(id=id).delete()
        return DeleteApplication(ok=True, application=application)


class DeletePoints(graphene.Mutation):
    ok = graphene.Boolean()
    points = graphene.Field(PointsNode)

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Points)
    def mutate(cls, root, info, id):
        points = Points.objects.get(id=id).delete()
        return DeletePoints(ok=True, points=points)


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
