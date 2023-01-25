from django.shortcuts import render,redirect,get_object_or_404
from users import forms
from .models import Contact
from .forms import ContactForm
from users.models import Customer
from products.forms import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login, logout as auth_logout,get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.conf.urls import handler404
from .serializers import ContactSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

# ------------------------------------------ Begin Home Page ----------------------------------------------------

# Home page
def index(request):
    products = Product.objects.all()
    categories=Category.objects.all()
    paginator = Paginator( products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    category = get_object_or_404(Category, pk=1)
    product_best_seller = Product.objects.filter(category=category).all()
    paginator1 = Paginator(product_best_seller, 3)
    page_number1 = request.GET.get('page')
    page_obj1 = paginator1.get_page(page_number1)
    category1 = get_object_or_404(Category, pk=2)
    product_best_seller2 = Product.objects.filter(category=category1).all()
    paginator2 = Paginator(product_best_seller2, 2)
    page_number2 = request.GET.get('page')
    page_obj2 = paginator2.get_page(page_number2)
    return render(request,'home/index.html',{'page_obj': page_obj,'categories':categories,'page_obj1': page_obj1,'page_obj2': page_obj2})

# Login page
def login(request):
    categories=Category.objects.all()
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
                return redirect('admin')
        else:
            messages.error(request,'Tài khoản hoặc mật khẩu không đúng!')
            return redirect('login')
    acount=forms.LoginForm()
    return render(request,'home/login.html', {'form':acount,'categories':categories})

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
            User.objects.create_user(username,email,password)
            account=Customer(username=username,email=email,password=password)
            account.save()
            messages.success(request,'Đăng ký tài khoản thành công')
            return redirect('login')
    else:
        categories=Category.objects.all()
        form=forms.RegisterForm()
    return render(request,'home/register.html',{'form':form,'categories':categories})

# Logout
def logout(request):
    auth_logout(request)
    messages.success(request,'Đăng xuất thành công')
    return redirect('/')

# Contact page
def contact(request):
    categories=Category.objects.all()
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ContactForm(request.POST)
            user= request.user
            customer = Customer.objects.filter(username=user.username).first()
            if form.is_valid():
                new_form = form.save(commit=False) # không thực hiện lưu đối tượng ngay lập tức mà thay vào đó có thể chỉnh sửa giá trị trước khi lưu.
                new_form.username = customer
                new_form.save()
                messages.success(request,'Phản hồi của bạn đã được gửi')
                return redirect('contact')     
        else:
            messages.error(request,'Bạn cần đăng nhập để liên hệ với chúng tôi!')
            return redirect('login')
    form = ContactForm()
    return render(request,'home/contact.html',{'categories':categories,'form':form})

# def page_not_found(request, exception):
#     return render(request, '404.html', {}, status=404)
# handler404 = page_not_found

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page ----------------------------------------------------

# Admin page
# @login_required(login_url='login')
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


# Show list Contact 
def contact_list(request):
    contacts = Contact.objects.all()
    paginator = Paginator(contacts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/contact_manager/contact_list.html', {'page_obj': page_obj})


# ------------------------------------------ End Admin Page ----------------------------------------------------

# ------------------------------------------ Begin RestAPI ----------------------------------------------------

# RestAPI Contact
class  Contact_API_View(APIView):
    def get(self,request):
        listContact= Contact.objects.all()
        Contactdata= ContactSerializer(listContact, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data= Contactdata, status=status.HTTP_200_OK)
    
# ------------------------------------------ End RestAPI ----------------------------------------------------