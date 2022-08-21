# Import necessary classes
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import OrderForm, InterestForm, RegisterForm
from .models import Topic, Course, Student, Order
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json
from django.utils import timezone


# Create your views here.

def index(request):
    # if request.session.test_cookie_worked():
    # request.session.delete_test_cookie()
    # return HttpResponse("You are logged in")
    top_list = Topic.objects.all().order_by('id')[:10]
    top_courses = Course.objects.all().order_by('-price')[:5]
    browserclose = request.session.get_expire_at_browser_close()
    if 'last_login' in request.session:
        last_login = request.session['last_login']
    else:
        last_login = 0
    return render(request, 'myapp/index.html',
                  {'top_list': top_list, 'course_list': top_courses, 'last_login': last_login,
                   'browserCLose': browserclose})


def about(request):
    about_visits = request.COOKIES.get('about_visits')
    if about_visits:
        cookie_count = int(about_visits) + 1
    else:
        cookie_count = 1
    about_response = render(request, 'myapp/about.html', {'count': cookie_count})
    about_response.set_cookie(key='about_visits', value=cookie_count, max_age=300)
    return about_response


def detail(request, top_no):
    topics = Topic.objects.get(id=top_no)
    t_category = topics.get_category_display()
    courses = Course.objects.filter(topic=top_no)
    # return render(request, 'myapp/detail0.html', {'topic_category': t_category})
    return render(request, 'myapp/detail.html',
                  {'topic_name': topics, 'topic_category': t_category, 'courses': courses})


def detail(request, top_no):
    topics = get_object_or_404(Topic, id=top_no)
    t_category = topics.get_category_display()
    courses = Course.objects.filter(topic=top_no)
    # return render(request, 'myapp/detail0.html', {'topic_category': t_category})
    return render(request, 'myapp/detail.html',
                  {'topic_name': topics, 'topic_category': t_category, 'courses': courses})


def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'courlist': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.levels <= order.course.stages:
                # order.save()
                if order.course.price > 150:
                    order.course.discount()
                order.save()
                msg = 'Your course has been ordered successfully.'
            else:
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
    return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg, 'courlist': courlist})


def coursedetail(request, cour_id):
    top_list = Topic.objects.all().order_by('id')[:10]
    top_courses = Course.objects.all().order_by('-price')[:5]
    course_detail = Course.objects.get(id=cour_id)
    interested = course_detail.interested
    if request.method == 'POST':
        myform = InterestForm(request.POST)
        if myform.is_valid():
            form_interested = myform.cleaned_data['interested']
            if int(form_interested) == 1:
                interested += 1
                course_detail.interested = interested
                course_detail.save()
                return render(request, 'myapp/index.html', {'top_list': top_list, 'top_course': top_courses})
                # msg = 'Your course has been ordered successfully.'
    else:
        myform = InterestForm()
    return render(request, 'myapp/coursedetail.html', {'form': myform, 'course_name': course_detail})
    # return render(request, 'myapp/coursedetail.html', {'course_name': course_detail})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            # return HttpResponse("You are logged in")
        request.session.set_test_cookie()

        now = datetime.datetime.now()
        json_str = json.dumps(now, default=str)
        request.session['last_login'] = json_str
        request.session.set_expiry(3600);

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('eLearnApp:myaccount'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    # logout(request)
    # del request.session['last_login']
    return HttpResponseRedirect(reverse('eLearnApp:user_login'))


@login_required(login_url='/eLearnApp/login/')
def myaccount(request):
    username = request.user
    try:
        curr_student = get_object_or_404(Student, username=username)
        sid = curr_student.id
        course_ordered = Order.objects.filter(student=sid)
        topic_interested = curr_student.interested_in.all()
        # topic_interested = Student.objects.filter(id=sid).values_list('interested_in__name', flat=True)
        return render(request, 'myapp/myaccount.html',
                      {'student': curr_student, 'orders': course_ordered, 'topics': topic_interested})

    except:
        return render(request, 'myapp/myaccount.html')


@login_required
def myorders(request):
    username = request.user
    try:
        curr_student = get_object_or_404(Student, username=username)
        sid = curr_student.id
        course_ordered = Order.objects.filter(student=sid)
        # topic_interested = curr_student.interested_in.all()
        # topic_interested = Student.objects.filter(id=sid).values_list('interested_in__name', flat=True)
        return render(request, 'myapp/myorder.html',
                      {'student': curr_student, 'orders': course_ordered})

    except:
        return render(request, 'myapp/myorder.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'myapp/login.html')

    form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('UserEmail')
        password = "passwordNew"
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        send_mail(
            "New Password",  # subject
            password,  # message
            '',  # from
            [email],  # to
        )
        return HttpResponse("We have emailed you a new password")
    else:
        return render(request, 'myapp/passwordreset.html')




#lancerguidewindsor@gmail.com