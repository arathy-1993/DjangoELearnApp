from django.shortcuts import redirect
from django.urls import path
from eLearnApp import views

app_name = 'eLearnApp'
urlpatterns = [
    path(r'', views.user_login, name='user_login'),
    path(r'index/', views.index, name='index'),
    path(r'about/', views.about, name='about'),
    path(r'<int:top_no>/', views.detail, name='detail'),
    path(r'courses/', views.courses, name='courses'),
    path(r'place_order/', views.place_order, name='place_order'),
    path(r'courses/<int:cour_id>/', views.coursedetail, name='course_detail'),
    path(r'login/', views.user_login, name='user_login'),
    path(r'logout/', views.user_logout, name='user_logout'),
    path(r'myaccount/', views.myaccount, name='myaccount'),
    path(r'register/', views.register, name='register'),
    path(r'myorder/', views.myorders, name='myorder'),
    path(r'forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path(r'myaccount//', lambda req: redirect('/myapp/myaccount/')),


]
