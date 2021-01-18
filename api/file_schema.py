import csv

import graphene
from django.db import transaction
from graphene_file_upload.scalars import Upload


class UploadMutation(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        file = Upload(required=True)

    @transaction.atomic
    def mutate(self, info, file, **kwargs):
        csv_reader = csv.reader(file, delimiter=',')
        for row in csv_reader:
            print(row)
        '''
        department_admin = request.user
        students_file = request.data['file']
        students_file = TextIOWrapper(students_file, encoding=request.encoding)
        csv_reader = csv.reader(students_file, delimiter=',')
        user_serializer = UserSerializer()
        for row in csv_reader:
            try:
                user = User.objects.get(email=row[0], university=department_admin.university,
                                        department=department_admin.department, groups_id=3)
            except api.models.User.DoesNotExist:
                user = user_serializer.create(
                    validated_data={'email': row[0], 'university': department_admin.university,
                                    'department': department_admin.department, 'groups_id': 3, 'password': "pass"})
            user = User.objects.get(email=row[0], university=department_admin.university,
                                    department=department_admin.department, groups_id=3)
            Student(user=user, field_of_study=FieldOfStudy.objects.get(name=row[1],
                                                                       year=Year.objects.get(start_year=int(row[2]),
                                                                                             department=department_admin.department))).save()
        '''
        return UploadMutation(success=True)
