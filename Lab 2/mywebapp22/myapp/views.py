from urllib import response
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Topic, Course, Student, Order

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    response = HttpResponse()
    heading1 = '<p>' + 'List of topics: ' + '</p>'
    response.write(heading1)
    for topic in top_list:
        para = '<p>'+ str(topic.id) + ': ' + str(topic) + '</p>'
        response.write(para)
    course_list = Course.objects.all().order_by('-price')[:5]
    heading2 = '<p>' + 'List of Courses: ' + '</p>'
    response.write(heading2)
    subheading2 = '<p>' + 'List of Courses: Price: Course Availability' + '</p>'
    for course in course_list:
        if course.for_everyone:
            avail = "This Course is For Everyone"
        else:
            avail = "This Course is Not For Everyone!"
        para = '<p>'+ str(course.name) + ': ' + str(course.price) + ': ' + str(avail) + '</p>'
        response.write(para)
    return response 

def about(request):
    response = HttpResponse()

    heading1 = '<p>' + 'This is an E-learning Website! Search our Topics to find all available Courses' + '</p>'
    response.write(heading1)
    return response

def detail(request, id):
    response = HttpResponse()
    topic = get_object_or_404(Topic,pk=id) 
    
    
    heading1 = '<p>' + 'List of courses under ' + topic.name + '</p>'
    response.write(heading1)
    subheading1='<p>' + 'Category: ' + topic.category + '</p>'
    response.write(subheading1)
    
    course_list = Course.objects.filter(topic=id)

    for course in course_list:
        if course.for_everyone:
            avail = "This Course is For Everyone"
        else:
            avail = "This Course is Not For Everyone!"
        para = '<p>'+ str(course.name) + ': ' + str(course.price) + ': ' + str(avail) + '</p>'
        response.write(para)

    return response