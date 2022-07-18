from django.urls import path
from myapp import views
app_name = 'myapp'

urlpatterns = [
 path(r'', views.index, name='index'),
 path(r'about', views.about, name='about'),
 path(r'courses', views.courses, name='courses'),
 path(r'detail/<id>/', views.detail, name='detail'),
 path(r'place_order', views.place_order, name='placeOrder'),
 path(r'courses/<int:cour_id>/', views.coursedetail, name='courseDetail'),
 path(r'user_login', views.user_login, name='user_login'),
 path(r'user_logout', views.user_logout, name='user_logout'),
 path(r'my_account', views.myaccount, name='myaccount')
]
