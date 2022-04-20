from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.http import request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
from django.views import View
from django.views.generic import TemplateView

from foodapp.models import Restaurant, Dish


# def index(request):
#     return render(request,'index.html')

class Index(TemplateView):
    template_name = "index.html"


def menu(request):
    return render(request,'restaurant.html')


def allDishRest(request,r_slug=None):
    r_page=None
    dishes_list=None
    if r_slug!=None:
        r_page=get_object_or_404(Restaurant,slug=r_slug)
        dishes_list=Dish.objects.all().filter(restaurant=r_page)
    else:
        dishes_list = Dish.objects.all().filter()
    paginator=Paginator(dishes_list,6)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        dishes=paginator.page(page)
    except (EmptyPage,InvalidPage):
        dishes=paginator.page(paginator.num_pages)
    return render(request,'restaurant.html',{'restaurant':r_page,'dishes':dishes})

def dishDetail(request,r_slug,dish_slug):
    try:
        dish=Dish.objects.get(restaurant__slug=r_slug,slug=dish_slug)
    except Exception as e:
        raise e
    return render(request,'dish.html',{'dish':dish})

#class based view for login page

class LoginView(View):
    def get(self,request):
        return render(request,"login.html")
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)

            return redirect('/')
        else:
            messages.info(request,'invalid credentials')
            return redirect('foodapp:loginview')


#class based view for registration
class RegisterView(View):
    def get(self,request):
        return render(request,"register.html")
    def post(self,request):
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
                return redirect('foodapp:registerview')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('foodapp:registerview')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name,
                                                last_name=last_name, email=email)
                # user=User.objects.create_user(username=username,password=password)
                user.save()
                # send_mail('Registration successful','Login to see more!!',settings.EMAIL_HOST_USER,[username])
                return redirect('foodapp:loginview')
        else:
            messages.info(request,'password is not matching...')
            return redirect('foodapp:registerview')


# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password = request.POST['password']
#         cpassword = request.POST['password1']
#         if password == cpassword:
#             if User.objects.filter(username=username).exists():
#                 messages.info(request, 'Username Taken')
#                 return redirect('foodapp:register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request, 'Email Taken')
#                 return redirect('foodapp:register')
#             else:
#                 user = User.objects.create_user(username=username, password=password, first_name=first_name,
#                                                 last_name=last_name, email=email)
#
#                 user.save();
#                 return redirect('foodapp:login')
#         else:
#             # print('password not matched')
#             messages.info(request, 'password not matching')
#             return redirect('foodapp:register')
#         return redirect('/')
#     return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')