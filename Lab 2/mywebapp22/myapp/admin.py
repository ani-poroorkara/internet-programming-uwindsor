from django.contrib import admin

# Register your models here.
from myapp.models import *

admin.site.register(Topic)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Order)
