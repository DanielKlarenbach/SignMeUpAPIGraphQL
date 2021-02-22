import graphene

from api.models import Department, Year, FieldOfStudy, Subject, Points, Application, University
from api.permissions import is_logged_in, is_objects_university_admin, \
    is_objects_department_admin, is_owner, is_university_admin
from api.retrieve_schema import DepartmentNode, YearNode, \
    FieldOfStudyNode, \
    SubjectNode, PointsNode, ApplicationNode, UserNode, \
    UniversityNode


class UpdateUser(graphene.Mutation):
    user = graphene.Field(UserNode)

    class Arguments:
        username = graphene.String(required=False)
        password = graphene.String(required=False)
        email = graphene.String(required=False)

    @classmethod
    @is_logged_in()
    def mutate(cls, root, info, **kwargs):
        user = info.context.user
        for k, v in kwargs.items():
            user.k = v
        user.save()
        return UpdateUser(user=user)


class UpdateUniversity(graphene.Mutation):
    university = graphene.Field(UniversityNode)

    class Arguments:
        name = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_university_admin()
    def mutate(cls, root, info, name):
        university_admin_user = info.context.user
        university = University.objects.get(university_admin__user=university_admin_user)
        university.name = name
        university.save()
        return UpdateUniversity(university)


class UpdateDepartment(graphene.Mutation):
    department = graphene.Field(DepartmentNode)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_university_admin(model=Department)
    def mutate(cls, root, info, id, name):
        department = Department.objects.get(id=id)
        department.name = name
        department.save()
        return UpdateDepartment(department)


class UpdateYear(graphene.Mutation):
    year = graphene.Field(YearNode)

    class Arguments:
        id = graphene.Int(required=True)
        start_year = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=Year)
    def mutate(cls, root, info, id, start_year):
        year = Year.objects.get(id=id)
        year.start_year = start_year
        year.save()
        return UpdateYear(year)


class UpdateFieldOfStudy(graphene.Mutation):
    field_of_study = graphene.Field(FieldOfStudyNode)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department')
    def mutate(cls, root, info, id, name):
        field_of_study = FieldOfStudy.objects.get(id=id)
        field_of_study.name = name
        field_of_study.save()
        return UpdateFieldOfStudy(field_of_study)


class UpdateSubject(graphene.Mutation):
    subject = graphene.Field(SubjectNode)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=False)
        description = graphene.String(required=False)
        lecturer = graphene.String(required=False)
        day = graphene.String(required=False)
        type = graphene.String(required=False)
        start_time = graphene.Time(required=False)
        end_time = graphene.Time(required=False)
        limit = graphene.Int(required=False)

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(Subject, lookup='field_of_study__year__department')
    def mutate(cls, root, info, id, **kwargs):
        subject = Subject.objects.get(id=id)
        for k, v in kwargs.items():
            subject.k = v
        subject.save()
        return UpdateSubject(subject)


class UpdatePoints(graphene.Mutation):
    points = graphene.Field(PointsNode)

    class Arguments:
        id = graphene.Int(required=True)
        points = graphene.String(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Points)
    def mutate(cls, root, info, id, points):
        subject_points = Points.objects.get(id=id)
        subject_points.points = points
        subject_points.save()
        return UpdatePoints(points)


class UpdateApplication(graphene.Mutation):
    application = graphene.Field(ApplicationNode)

    class Arguments:
        id = graphene.Int(required=True)
        priority = graphene.Int(required=True)

    @classmethod
    @is_logged_in()
    @is_owner(model=Application)
    def mutate(cls, root, info, id, priority):
        application = Application.objects.get(id=id)
        application.priority = priority
        application.save()
        return UpdatePoints(priority)


class Mutation(graphene.ObjectType):
    update_user = UpdateUser.Field()
    update_university = UpdateUniversity.Field()
    update_department = UpdateDepartment.Field()
    update_year = UpdateYear.Field()
    update_field_of_study = UpdateFieldOfStudy.Field()
    update_subject = UpdateSubject.Field()
    update_points = UpdatePoints.Field()
    update_application = UpdateApplication
