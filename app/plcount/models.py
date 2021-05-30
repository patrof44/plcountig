from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db.models.fields import DateField
from django.db.models.query import QuerySet
from .validator import file_size



class fluxo(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
	entradas=models.IntegerField()
	saidas=models.IntegerField()
	data = models.DateField(auto_now_add=True, null=True)


	def __str__(self):
		return self.user
	

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name_company = models.CharField(max_length=200)
	nif_company = models.IntegerField()
	address_company = models.CharField(max_length=200)
	phone = models.IntegerField()

	def __str__(self):
		return self.user.username

class Video(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name_company = models.CharField(max_length=100)
	date = models.DateField()
	video = models.FileField(upload_to="video/%y", validators=[file_size])

	def __str__(self):
		return self.name_company

class Home(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(max_length=100)
	title = models.CharField(max_length=100)
	message = models.CharField(max_length=500)

	def __str__(self):
		return self.title

class Report(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField()
	report = models.FileField(upload_to="report/%y", validators=[file_size])

	def __str__(self):
		return self.user.username





# Create your models here.