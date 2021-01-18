import csv
import random
import string
from io import TextIOWrapper

import graphene
import pandas
from django.contrib.auth import get_user_model
from django.db import transaction

from api.models import Department, FieldOfStudy, Student
from api.permissions import is_department_admin, is_logged_in

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

class UploadFile(graphene.ClientIDMutation):
    success = graphene.String()

    class Input:
        pass

    @classmethod
    @transaction.atomic
    @is_logged_in()
    @is_department_admin()
    def mutate_and_get_payload(cls, root, info, **input):
        file = info.context.FILES['file']
        df = pandas.read_csv(file)
        user=info.context.user
        department=Department.objects.get(department_admins__user=user)
        for i in range (0,len(df)):
            try:
                field_of_study=FieldOfStudy.objects.get(name=df['field_of_study'][i],year__department=department,year__start_year=df['year'][i])
            except FieldOfStudy.DoesNotExist:
                raise Exception("This field of study doesn't exist "+str(df['field_of_study'][i])+str(df['year'][i]))
            try:
                user=get_user_model().objects.get(email=df['email'][i])
            except get_user_model().DoesNotExist:
                user = get_user_model()(username=df['username'][i], email=df['email'][i])
                user.set_password(get_random_string(10))
                user.save()
            Student.objects.create(user=user,field_of_study=field_of_study)
        return UploadFile("Upload successful")


class Mutation(graphene.ObjectType):
    upload_file = UploadFile.Field()
