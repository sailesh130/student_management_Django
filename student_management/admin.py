from django.contrib import admin
from .models import CustomUser,Student,Faculty,Subject,Supervisior
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Subject)
admin.site.register(Supervisior)