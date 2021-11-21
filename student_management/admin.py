from django.contrib import admin
from .models import Student, Supervisior, Subject, Faculty

# Register your models here.
admin.site.register(Student)
admin.site.register(Supervisior)
admin.site.register(Subject)
admin.site.register(Faculty)
