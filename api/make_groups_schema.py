import random

import graphene
from django.db.models import Max

from api.models import FieldOfStudy, Subject, Student, Points, SubjectGroup
from api.permissions import is_logged_in, is_objects_department_admin


class MakeGroups(graphene.Mutation):
    class Arguments:
        field_of_study_id = graphene.Int(required=True, name='fieldOfStudyId')

    @classmethod
    @is_logged_in()
    @is_objects_department_admin(model=FieldOfStudy, lookup='year__department', id_kwarg='field_of_study_id')
    def mutate(cls, root, info, field_of_study_id):
        subjects_names = Subject.objects.filter(field_of_study_id=field_of_study_id, type='P').values_list(
            'name').distinct()

        for subject_name in subjects_names:
            subjects_with_free_places = Subject.objects.filter(field_of_study_id=field_of_study_id, type='P')
            students_without_subject_group = Student.objects.filter(field_of_study_id=field_of_study_id)
            points_by_subject = Points.objects.filter(subject__name=subject_name)
            current_max = points_by_subject.aggregate(Max('points'))
            while current_max != 0:
                points_by_current_max = list(points_by_subject.filter(points=current_max))
                random.shuffle(points_by_current_max)
                for points in points_by_current_max:
                    subject = Subject.objects.get(id=points.subject_id)
                    student = Student.objects.get(id=points.student_id)
                    subject_group = SubjectGroup.objects.get(subject=subject, student=student)
                    if subject.occupancy != subject.limit and subject_group is None:
                        SubjectGroup(subject=subject, student=student).save()
                        students_without_subject_group.exclude(id=student.id)
                    elif subject.occupancy == subject.limit:
                        subjects_with_free_places.exclude(id=subject.id)
            for student in students_without_subject_group:
                for subject_with_free_places in subjects_with_free_places:
                    SubjectGroup(subject=subject_with_free_places, student=student).save()
                    if subject_with_free_places.occupancy == subject_with_free_places.limit:
                        subjects_with_free_places.exclude(id=subject_with_free_places.id)


class Mutation(graphene.ObjectType):
    make_groups = MakeGroups.Field()