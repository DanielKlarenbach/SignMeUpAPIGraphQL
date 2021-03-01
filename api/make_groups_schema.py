import random

import graphene
from django.db.models import Max, Q

from api.models import FieldOfStudy, Subject, Student, Points, SubjectGroup
from api.permissions import is_logged_in, is_objects_department_admin


class MakeGroups(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        field_of_study_id = graphene.Int(required=True, name='fieldOfStudyId')

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department', id_kwarg='field_of_study_id')
    def mutate(cls, root, info, field_of_study_id):
        subjects_types = Subject.objects.filter(field_of_study_id=field_of_study_id, type='P').values_list(
            'name').distinct()

        for subject_type in subjects_types:
            subjects_without_free_places = []
            students_with_subject_group = []

            points_by_subject_type = Points.objects.filter(subject__name=subject_type[0],
                                                           subject__field_of_study_id=field_of_study_id)
            current_max = points_by_subject_type.aggregate(Max('points'))
            current_max = current_max['points__max']
            while current_max != 0:
                points_by_current_max = list(points_by_subject_type.filter(points=current_max))
                random.shuffle(points_by_current_max)
                for points in points_by_current_max:
                    subject = Subject.objects.get(id=points.subject_id)
                    student = Student.objects.get(id=points.student_id)

                    subject_group = SubjectGroup.objects.filter(subject__name=subject_type[0], student=student)
                    if subject.occupancy != subject.limit and not subject_group:
                        SubjectGroup(subject=subject, student=student).save()
                        students_with_subject_group.append(student.id)
                    if subject.occupancy == subject.limit:
                        subjects_without_free_places.append(subject.id)
                current_max -= 1

            subjects_with_free_places = Subject.objects.filter(field_of_study_id=field_of_study_id, type='P').filter(
                ~Q(id__in=subjects_without_free_places))
            students_without_subject_group = Student.objects.filter(field_of_study_id=field_of_study_id).filter(
                ~Q(id__in=students_with_subject_group))
            for student in students_without_subject_group:
                for subject_with_free_places in subjects_with_free_places:
                    SubjectGroup(subject=subject_with_free_places, student=student).save()
                    if subject_with_free_places.occupancy == subject_with_free_places.limit:
                        subjects_with_free_places = subjects_with_free_places.exclude(id=subject_with_free_places.id)
        return MakeGroups(ok=True)


class Mutation(graphene.ObjectType):
    make_groups = MakeGroups.Field()
