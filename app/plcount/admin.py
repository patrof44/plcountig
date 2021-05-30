from django.contrib import admin
from plcount.models import UserProfile
from .models import Report, Video, Home

admin.site.register(UserProfile)

admin.site.register(Video)

admin.site.register(Home)

admin.site.register(Report)

# Register your models here.
