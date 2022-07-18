from unicodedata import category
from urllib import response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Topic, Course, Student, Order
from datetime import datetime

from .forms import *

# Create your views here.
def index(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 'Your last login was more than one hour ago'
    return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login})
    #return render(request, 'myapp/index.html', {'top_list': top_list})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})

def about(request):
    if 'about_visits' in request.session:
        request.session['about_visits'] += 1
    else:
        request.session['about_visits'] = 1
        request.session.set_expiry(300)
    return render(request, 'myapp/about.html', {'about_visits': request.session['about_visits']})
    #return render(request, 'myapp/about.html')

def detail(request, id):
    response = HttpResponse()
    topic = get_object_or_404(Topic,pk=id) 
    
    name = topic.name
    category = topic.category

    course_list = Course.objects.filter(topic=id)

    return render(request, 'myapp/detail.html', {'name': name,'course_list': course_list, 'category':category})

def place_order(request):
    msg = ''
    course_list = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                order.save()
                msg = 'Your course has been ordered successfully.'
                if order.course.price > 150.00:
                    order.course.discount();
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg })
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'course_list': course_list})

def coursedetail(request, cour_id):
    course = get_object_or_404(Course, pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["interested"] == "1":
                course.interested = course.interested+1
                course.save()
                return redirect('/myapp/')
            else:
                return  redirect('/myapp/')
        else:
            msg = 'There was an error in saving. Please try again'
            return redirect(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = InterestForm()
        return render(request, 'myapp/coursedetail.html', {'form': form, 'course': course})
    
def user_login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            print("test cookie worked")
        else:
            print("test cookie didn't work")
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime("%H:%M:%S - %B %d, %Y")
                # request.session.set_expiry(3600)
                request.session.set_expiry(0)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        request.session.set_test_cookie()
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    # logout(request)
    # request.session.flush()
    for key in list(request.session.keys()):
        del request.session[key]
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def myaccount(request):
    students = Student.objects.filter(pk=request.user.id)
    if len(students) == 1:
        student = students[0]
        return render(request, 'myapp/my_account.html', {'fullName': student.first_name + " " + student.last_name,
                                                         'orders': student.orders.all(),
                                                         'interested_in': student.interested_in.all()
                                                         })
    else:
        return HttpResponse('You are not a registered student!')
