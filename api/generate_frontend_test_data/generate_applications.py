import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SignMeUpAPIGraphQL.settings')
import django

django.setup()

from api.models import Student, FieldOfStudy, Subject, Application, SubjectGroup

if __name__ == '__main__':
    Application.objects.all().delete()
    SubjectGroup.objects.all().delete()
    field_of_study=FieldOfStudy.objects.all()[0]
    students = Student.objects.filter(field_of_study=field_of_study)[0:2]
    subjects = Subject.objects.filter(subject_type__field_of_study=field_of_study)[0:2]
    SubjectGroup(student=students[0],subject=subjects[0]).save()
    SubjectGroup(student=students[1],subject=subjects[1]).save()
    Application(unwanted_subject=subjects[0],wanted_subject=subjects[1],student=students[0]).save()
    print(students[1])
    print(subjects[0].id,subjects[1].id)