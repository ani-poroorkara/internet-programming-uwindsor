from unicodedata import category
from urllib import response
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import Topic, Course, Student, Order

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, id):
    response = HttpResponse()
    topic = get_object_or_404(Topic,pk=id) 
    
    name = topic.name
    category = topic.category

    course_list = Course.objects.filter(topic=id)

    # for course in course_list:
    #     if course.for_everyone:
    #         avail = "This Course is For Everyone"
    #     else:
    #         avail = "This Course is Not For Everyone!"
    #     para = '<p>'+ str(course.name) + ': ' + str(course.price) + ': ' + str(avail) + '</p>'
    #     response.write(para)

    return render(request, 'myapp/detail.html', {'name': name,'course_list': course_list, 'category':category})

def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = Order(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = Order()
    return render(request, 'myapp/placeorder.html', {'form':form, 'msg':msg, 'courlist':courlist})
