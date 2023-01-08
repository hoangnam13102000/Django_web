from django.shortcuts import render,redirect,get_object_or_404
from users import forms
from users.models import Customer
from products.forms import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout,get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import allowed_user
from django.core.paginator import Paginator

# Create your views here.

# Home page
def index(request):
    products = Product.objects.all()
    categories=Category.objects.all()
    paginator = Paginator( products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home/index.html',{'page_obj': page_obj,'categories':categories})

# Admin page
@login_required(login_url='login')
def index_admin(request):
    cusromers = Customer.objects.all()
    paginator = Paginator(cusromers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    products = Product.objects.all()
    paginator1 = Paginator(products, 5)
    page_number1 = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)
    return render(request,'admin/index.html',{'page_obj': page_obj,'page_obj1': page_obj1})

# Contact page
def contact(request):
    categories=Category.objects.all()
    return render(request,'home/contact.html',{'categories':categories})

# Login page
def login(request):
    acount=forms.LoginForm()
    if(request.method=="POST"):
        username=request.POST['username']
        password=request.POST['password']
        user =authenticate(request, username=username,password=password )
        if(user is not None):
            get_user= get_user_model()
            role=get_user.objects.get(username= username)
            if(role.is_staff == False):
                auth_login(request,user)
                messages.success(request,'Đăng nhập thành công')
                return redirect('home')
            else:
                messages.success(request,'Đăng nhập trang Admin thành công')
                auth_login(request,user)
                return redirect('index_admin')
        else:
            messages.error(request,'Tài khoản hoặc mật khẩu không đúng!')
            return redirect('login')
    acount=forms.LoginForm()
    return render(request,'home/login.html', {'form':acount})

# Register page
def register(request):
    form=forms.RegisterForm()
    if(request.method=="POST"):
        form=forms.RegisterForm(request.POST)
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if(User.objects.filter(username=username)):
            messages.error(request,'Tên đăng nhập đã tồn tại!')
            return redirect('register')
        if(User.objects.filter(email=email)):
            messages.error(request,'Email đã tồn tại!')
            return redirect('register')
        if(password!=password2):
             messages.error(request,'Mật khẩu không trùng nhau!')
             return redirect('register')
        if(form.is_valid()):
            user=User.objects.create_user(username,email,password)
            account=Customer(username=username,email=email,password=password)
            account.save()
            messages.success(request,'Đăng ký tài khoản thành công')
            return redirect('login')
    else:
        form=forms.RegisterForm()
    return render(request,'home/register.html',{'form':form})

# Logout
def logout(request):
    auth_logout(request)
    messages.success(request,'Đăng xuất thành công')
    return redirect('/')

