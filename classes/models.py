from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

class Classroom(models.Model):
	teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=120)
	year = models.IntegerField()

	def get_absolute_url(self):
		return reverse('classroom-detail', kwargs={'classroom_id':self.id})

# gender_options=('Male','Female')
class Student(models.Model):
	STATUS_CHOICES = (
        ('MALE', 'Male'),
        ('FEMALE','Female'))
	classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='students')
	name = models.CharField(max_length=120)
	date_of_birth = models.CharField(max_length=120)
	exam_grade = models.PositiveIntegerField(primary_key=True, validators=[MaxValueValidator(100)])
	gender = models.CharField(max_length=20, choices=STATUS_CHOICES)
	def __str__(self):
		return self.name

    