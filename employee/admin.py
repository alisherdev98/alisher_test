from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Employee, UserAdmin)
admin.site.register(Job_position)
