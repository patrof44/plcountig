from plcount.validator import file_size
from typing import ClassVar
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Report, UserProfile, Video, Home
from django.forms.widgets import NumberInput

class ExtendedUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

	def save(self, commit=True):
		user = super().save(commit=False)

		user.email = self.cleaned_data['email']
		user.first_name = self.cleaned_data['first_name']
		user.last_name  = self.cleaned_data['last_name']

		if commit:
			user.save()
		return user

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('name_company', 'nif_company', 'address_company', 'phone')
		
class UserUpdateForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ('email','first_name','last_name')

class UserProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('name_company', 'nif_company', 'address_company', 'phone')

class VideoForm(forms.ModelForm):
	date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
	class Meta:
		model = Video
		fields = ('name_company','date','video')

class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ('name', 'email', 'title', 'message')


        widgets={
        'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nome' }),
        'email': forms.TextInput(attrs={'class': 'form-control','placeholder':'E-mail'}),
        'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Assunto'}),
        'message': forms.Textarea(attrs={'class': 'form-control','placeholder':'Mensagem'}), 
        }

class ReportForm(forms.ModelForm):
	class Meta:
		model = Report
		fields = ('date','report')

		
