from django.conf import settings
from django.db import models


# Create your models here.

class UniversityAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='university_admin', on_delete=models.CASCADE,
                                unique=True)

    class Meta:
        db_table = 'university_admins'

    def __str__(self):
        return f"{self.user}"


class University(models.Model):
    university_admin = models.OneToOneField(UniversityAdmin, on_delete=models.CASCADE, related_name='university',
                                            null=True, unique=True)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'universities'

    def __str__(self):
        return f"University: {self.name}"


class Department(models.Model):
    university = models.ForeignKey(University, related_name='departments', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'departments'
        constraints = [
            models.UniqueConstraint(fields=['university', 'name'], name='unique_department')
        ]

    def __str__(self):
        return f"{self.university} Department: {self.name}"


class Year(models.Model):
    department = models.ForeignKey(Department, related_name='years', on_delete=models.CASCADE)
    start_year = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'years'
        constraints = [
            models.UniqueConstraint(fields=['department', 'start_year'], name='unique_year')
        ]

    def __str__(self):
        return f"{self.department} Year: {self.start_year}"


class FieldOfStudy(models.Model):
    year = models.ForeignKey(Year, related_name='fields_of_study', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'fields_of_study'
        constraints = [
            models.UniqueConstraint(fields=['year', 'name'], name='unique_field_of_study')
        ]

    def __str__(self):
        return f"{self.year} Field of study: {self.name}"


class Subject(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy, related_name='subjects', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=50)
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"
    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday')
    ]
    day = models.CharField(max_length=15, choices=DAY_CHOICES)
    LECTURE = "L"
    PRACTICE = "P"
    TYPE_CHOICES = [
        (LECTURE, 'Lecture'),
        (PRACTICE, 'Practice')
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    occupancy = models.PositiveSmallIntegerField(default=0)
    limit = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'subjects'
        constraints = [
            models.UniqueConstraint(fields=['field_of_study', 'name'], name='unique_subject')
        ]

    def __str__(self):
        return f"{self.field_of_study} Subject: {self.name} Day: {self.day} Time: {self.start_time}:{self.end_time}"


class DepartmentAdmin(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='department_admin', on_delete=models.CASCADE,
                                unique=True)
    department = models.ForeignKey(Department, related_name='department_admins', on_delete=models.CASCADE)

    class Meta:
        db_table = 'department_admins'

    def __str__(self):
        return f"{self.user} {self.department}"


class Student(models.Model):
    field_of_study = models.ForeignKey(FieldOfStudy, related_name='students', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='students', on_delete=models.CASCADE)

    class Meta:
        db_table = 'students'
        constraints = [
            models.UniqueConstraint(fields=['field_of_study', 'user'], name='unique_student')
        ]

    def __str__(self):
        return f"{self.user} {self.field_of_study}"


class Points(models.Model):
    subject = models.ForeignKey(Subject, related_name='points', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='points', on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'points'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_points')
        ]

    def save(self, *args, **kwargs):
        if self.student.field_of_study != self.subject.field_of_study:
            raise Exception("Student can't assign points to the subject outside of his field of study")
        super(Points, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} {self.student}"


class Application(models.Model):
    unwanted_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="unwanted_applications")
    wanted_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="wanted_applications")
    student = models.ForeignKey(Student, related_name='applications', on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'applications'
        constraints = [
            models.UniqueConstraint(fields=['unwanted_subject', 'wanted_subject', 'student'], name='unique_application')
        ]

    def save(self, *args, **kwargs):
        if self.student.field_of_study != self.unwanted_subject.field_of_study or self.student.field_of_study != self.wanted_subject.field_of_study:
            raise Exception("Student can't make application with subject outside of his field of study")
        super(Application, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.unwanted_subject}->{self.wanted_subject} {self.student}"


class SubjectGroup(models.Model):
    subject = models.ForeignKey(Subject, related_name='subject_groups', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='subject_groups', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subject_groups'
        constraints = [
            models.UniqueConstraint(fields=['subject', 'student'], name='unique_subject_group')
        ]

    def save(self, *args, **kwargs):
        if self.student.field_of_study != self.subject.field_of_study:
            raise Exception("Student can't belong to the group outside of his field of study")
        super(SubjectGroup, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject} {self.student}"
