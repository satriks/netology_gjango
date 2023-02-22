from django.contrib import admin

# Register your models here.
from students.models import Course, Student

admin.site.register(Course)
admin.site.register(Student)
