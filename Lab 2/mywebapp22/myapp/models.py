from sre_constants import CATEGORY
from unicodedata import category
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    hours = models.CharField(max_length=5, null=True, blank=True)
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    interested = models.PositiveIntegerField(default=False)
    stages = models.PositiveIntegerField(default=False)

    def discount(self):
        self.price %= 10

    def __str__(self):
        return self.name

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
    ('CG', 'Calgery'),
    ('MR', 'Montreal'),
    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Order(models.Model):
    course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE)
    Student = models.ForeignKey(Student, related_name='orders', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(null=True, blank=True)
    status = [('0','Cancelled'), ('1','Order Confirmed')]
    order_status = models.CharField(max_length=20, choices=status, default='1')
    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Student.first_name + ' ' + self.Student.last_name

    def _get_total(self):
        return (self.levels * self.course.price)
