"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plcount import views

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexPage, name="home"),
    path('dashboard/<int:user_id>/', views.dashboardPage, name="dashboard"),
    path('chart/<int:user_id>/', views.chartPage, name="chart"),
    path('table/<int:user_id>/',views.tablePage, name="table"),
    path('video/<int:user_id>/', views.videoPage, name="video"),
    path('relatorio/<int:user_id>/', views.relatorioPage, name="relatorio"),
    path('calendar/<int:user_id>/', views.calendarPage, name="calendar"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
    path('profile/<int:user_id>/', views.profilePage, name="profile"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
