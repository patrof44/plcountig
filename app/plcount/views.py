from django import http
from django.http.response import HttpResponse, HttpResponseForbidden
from .models import UserProfile, fluxo, Video, Home, Report
from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from .forms import ExtendedUserCreationForm, ReportForm, UserProfileForm, UserProfileUpdateForm, UserUpdateForm, VideoForm, HomeForm
from django.db.models.aggregates import Sum
from django.forms.widgets import NumberInput


# Create your views here.


def indexPage(request):
	form=HomeForm(data=request.POST)
	if request.method == "POST":
		if form.is_valid():
			fs= form.save(commit=False)
			fs.save()
			messages.success(request, "A sua mensagem foi enviada com sucesso")
			return redirect('home')
		else:
			form=HomeForm()	

	context={
		'form' : form
	}
	return render(request, 'plcount/home.html', context )



@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def dashboardPage(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
        fluxos=fluxo.objects.filter(user=user)
        perfil = UserProfile.objects.get(user=user)

        totalSaidas = fluxo.objects.filter(user=user).aggregate(Sum('saidas'))['saidas__sum']
        totalEntradas = fluxo.objects.filter(user=user).aggregate(Sum('entradas'))['entradas__sum']

        context ={
			'totalSaidas': totalSaidas,
			'totalEntradas': totalEntradas,
			'fluxos': fluxos,
			'user': user,
			'perfil': perfil
		}

        return render(request, 'plcount/dashboard.html', context)
    else:
	    return HttpResponseForbidden()



@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def chartPage(request,user_id):
	user = User.objects.get(id=user_id)
	if request.user == user:
		fluxos=fluxo.objects.filter(user=user)

		context ={
				'fluxos': fluxos,
				'user': user,
			}
		return render(request, 'plcount/chart.html', context)
	else:
		return HttpResponseForbidden()

@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def tablePage(request, user_id):
	user = User.objects.get(id=user_id)
	if request.user == user:
		if request.method == "POST":
			result=fluxo.objects.all()
			request.GET.get('data')

			fromdate=request.POST.get('fromdate')
			todate=request.POST.get('todate')
			result = result.filter(data__gt=fromdate , data__lt=todate)

		
			return render(request, 'plcount/table.html', {'fluxos': result})

		else:
			fluxos=fluxo.objects.filter(user=user)
			perfil = UserProfile.objects.get(user=user)
				
			context ={
				'fluxos': fluxos,
				'user': user,
				'perfil': perfil
			}
			return render(request, 'plcount/table.html', context)
	else:
		return HttpResponseForbidden()


@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def videoPage(request, user_id):
	user = User.objects.get(id=user_id)
	if request.user == user:
		if request.method == "POST":
			form=VideoForm(data=request.POST,files=request.FILES)
			if form.is_valid():
				 fs= form.save(commit=False)
				 fs.user= request.user
				 fs.save()
				 messages.success(request, "Video enviado com sucesso! | Obrigado pela sua submissão")
				 return redirect('video', user_id=user.id)
		else:
			form=VideoForm()

		context	= {'user': user, 'form' : form}
		return render(request, 'plcount/video.html', context)
	else:
		return HttpResponseForbidden()

@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def relatorioPage(request, user_id):
	user = User.objects.get(id=user_id)
	if request.user == user: 	
		all_report = Report.objects.filter(user=user)
		form=ReportForm(files=request.FILES)
		

		context	= {'user': user, 'form' : form, 'all_report': all_report}
		return render(request, 'plcount/relatorio.html', context)
	else:
		return HttpResponseForbidden()

@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
def calendarPage(request, user_id):
	user = User.objects.get(id=user_id)
	if request.user == user: 	
		return render(request, 'plcount/calendar.html', {'user': user})
	else:
		return HttpResponseForbidden()


def registerPage(request):
	if request.method == 'POST':
		form = ExtendedUserCreationForm(request.POST)
		profile_form = UserProfileForm(request.POST)

		if form.is_valid() and profile_form.is_valid():
			user = form.save()

			profile = profile_form.save(commit=False)
			profile.user= user 

			profile.save()

			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=password)
			login(request, user)

			return redirect('index')

	else:
		form = ExtendedUserCreationForm()
		profile_form = UserProfileForm()

	context	= {'form' : form, 'profile_form' : profile_form}
	return render(request, 'plcount/register.html', context)

			

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
			
            return redirect('dashboard', user_id = user.id)
        else:
            messages.info(request, 'Username Ou password está incorreto')

    context = {}
    return render(request, 'plcount/login.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['cliente'])
@login_required
def profilePage(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user == user:
	    if request.method == 'POST':
		    u_form = UserUpdateForm(request.POST, instance=request.user)
		    p_form = UserProfileUpdateForm(request.POST, instance=request.user.userprofile)
		    if u_form.is_valid() and p_form.is_valid():
			    u_form.save()
			    p_form.save()
			    messages.success(request, "Os dados da sua conta foram atualizados")

	    else:
		    u_form = UserUpdateForm(instance=request.user)
		    p_form = UserProfileUpdateForm(instance=request.user.userprofile)

	    context = {
			'u_form': u_form,
			'p_form': p_form,
			'user': user
		}
	    return render(request, 'plcount/profile.html', context)
    else:
	    return HttpResponseForbidden()








    
# Create your views here.
