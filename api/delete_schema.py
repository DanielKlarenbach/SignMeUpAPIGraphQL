import graphene
from django.contrib.auth.models import User

from api.models import UniversityAdmin, DepartmentAdmin, Department, Year, FieldOfStudy, Subject, Student, SubjectGroup, \
    Application, Points
from api.permissions import is_logged_in, is_objects_university_admin, is_objects_department_admin_by_department, \
    is_owner, is_objects_department_admin_by_department_admin


class DeleteUniversityAdmin(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_university_admin(model=UniversityAdmin)
    def mutate(cls, root, info, id):
        return DeleteDepartmentAdmin(success_message="Deletion of admin: " + str(
            DepartmentAdmin.objects.get(id=id).user.delete()) + "successful")


class DeleteDepartmentAdmin(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_university_admin(model=DepartmentAdmin)
    def mutate(cls, root, info, id):
        return DeleteDepartmentAdmin(success_message="Deletion of department admin: " + str(
            DepartmentAdmin.objects.get(id=id).user.delete()) + "successful")


class DeleteDepartment(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_university_admin(model=Department)
    def mutate(cls, root, info, id):
        return DeleteDepartment(
            success_message="Deletion of department: " + str(Department.objects.get(id=id).delete()) + " successful")


class DeleteYear(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_department_admin_by_department_admin(model=Year)
    def mutate(cls, root, info, id):
        return DeleteYear(success_message="Deletion of year: " + str(Year.objects.get(id=id).delete()) + " successful")


class DeleteFieldOfStudy(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_department_admin_by_department_admin(model=FieldOfStudy)
    def mutate(cls, root, info, id):
        return DeleteFieldOfStudy(success_message="Deletion of field of study: " + str(
            FieldOfStudy.objects.get(id=id).delete()) + " successful")


class DeleteSubject(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_department_admin_by_department_admin(model=Subject)
    def mutate(cls, root, info, id):
        return DeleteSubject(
            success_message="Deletion of subject: " + str(Subject.objects.get(id=id).delete()) + " successful")


class DeleteStudent(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_department_admin_by_department_admin(model=Student)
    def mutate(cls, root, info, id):
        return DeleteStudent(
            success_message="Deletion of student: " + str(Student.objects.get(id=id).delete()) + " successful")


class DeleteSubjectGroup(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_objects_department_admin_by_department_admin(model=SubjectGroup)
    def mutate(cls, root, info, id):
        return DeleteSubjectGroup(success_message="Deletion of subject group: " + str(
            SubjectGroup.objects.get(id=id).delete()) + " successful")


class DeleteApplication(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_owner(model=Application)
    def mutate(cls, root, info, id):
        return DeleteApplication(
            success_message="Deletion of application: " + str(Application.objects.get(id=id).delete()) + " successful")


class DeletePoints(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_owner(model=Points)
    def mutate(cls, root, info, id):
        return DeletePoints(
            success_message="Deletion of points: " + str(Points.objects.get(id=id).delete()) + " successful")


class DeleteUser(graphene.Mutation):
    success_message = graphene.String()

    class Arguments:
        id = graphene.Int(required=True)

    @classmethod
    @is_logged_in
    @is_owner(model=User)
    def mutate(cls, root, info, id):
        return DeleteUser(
            success_message="Deletion of user: " + str(User.objects.get(id=id).delete()) + " successful")


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
