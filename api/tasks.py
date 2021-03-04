from django.db import transaction

from SignMeUpAPIGraphQL.celery import app
from api.models import Application, SubjectGroup


@app.task
@transaction.atomic
def check_for_matching_application(application_id):
    application=Application.objects.get(id=application_id)
    matching_applications = Application.objects.filter(unwanted_subject=application.wanted_subject,
                                                       wanted_subject=application.unwanted_subject).order_by(
        'created_at')
    if not matching_applications is None:
        matching_application = matching_applications[0]
        SubjectGroup.objects.get(student=application.student, subject=application.unwanted_subject).delete()
        SubjectGroup.objects.get(student=matching_application.student,
                                 subject=matching_application.unwanted_subject).delete()
        s1=SubjectGroup(student=application.student, subject=application.wanted_subject).save()
        SubjectGroup(student=matching_application.student, subject=matching_application.wanted_subject).save()
