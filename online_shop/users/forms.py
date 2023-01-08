from django import forms
from django.contrib.auth.models import User
from .models import Customer

class LoginForm(forms.Form):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Tên đăng nhập'}))
    password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu'}))
    

class RegisterForm(forms.Form):
    username=forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Tên đăng nhập'}))
    password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu'}))
    password2=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Xác nhận mật khẩu'}))
    email=forms.EmailField(max_length=50,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
   

class CustomerForm(forms.ModelForm):
    new_password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu cũ','required':''}))
    password2=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Xác nhận mật khẩu','required':''}))
    class Meta:
        model=Customer
        fields= ["fullname","gender","address","phone", "email","username","password"]
        choices_gender=(('Nam','Nam'),('Nữ','Nữ'))
        widgets={
            'fullname':forms.TextInput(attrs={'class':'form-control','placeholder':'Họ và tên'}),
            'gender': forms.RadioSelect(choices=choices_gender,attrs={'class':'form-check'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control','readonly':'','required':''}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu','required':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email','required':''}),
        }
class Customer_info_Form(forms.ModelForm):
    class Meta:
        model=Customer
        fields= ["fullname","gender","address","phone", "email","username"]
        choices_gender=(('Nam','Nam'),('Nữ','Nữ'))
        widgets={
            'fullname':forms.TextInput(attrs={'class':'form-control','placeholder':'Họ và tên'}),
            'gender': forms.RadioSelect(choices=choices_gender,attrs={'class':'form-check'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control','readonly':''}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
        }
class Change_Password_Form(forms.ModelForm):
    old_password=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu cũ'}))
    password2=forms.CharField(max_length=50,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Xác nhận khẩu'}))
    class Meta:
        model=Customer
        fields= ["password"]
        widgets={
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Mật khẩu mới','required':''}),
        }