from django.shortcuts import render,redirect, get_object_or_404 # calls the given model and get object from that if that object or model doesn’t exist it raise 404 error.
from .forms import CustomerForm,Customer_info_Form,Change_Password_Form
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Customer, Employee
from products.models import Category
from django.core.paginator import Paginator
from .forms import AddCustomerForm,AddEmployeeForm,EmployeeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from .serializers import CustomerSerializer #,CustomerCreationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# ------------------------------------------ Begin Home Page ----------------------------------------------------

# edit customer
def edit_info(request,id):
    user = get_object_or_404(User, id=id)
    customer=Customer.objects.filter(username=user.username).first() #first() takes a query set and returns the first element
    if(request.method=="POST"):
        form =Customer_info_Form(request.POST,instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request,'Đã cập nhập khách hàng thành công')
            return redirect("home")
        # print(form.errors) #print error of form
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'home/edit_info.html', {'form':form})

# Change password
def change_password(request, id):
    categories=Category.objects.all()
    user = get_object_or_404(User, id=id)
    customer=Customer.objects.filter(username=user.username).first()
    form =Change_Password_Form(request.POST)
    if form.is_valid():
        new_password=request.POST['password']
        old_password=request.POST['old_password']
        password2=request.POST['password2']
        if(customer.password == old_password):
            if(old_password==new_password):
                messages.error(request,'Mật khẩu mới không được trùng với mật khẩu cũ!')
                return redirect('change_password', id=user.id)
            else:
                if(new_password!=password2):
                    messages.error(request,'Mật khẩu không trùng nhau!')
                    return redirect('change_password', id=user.id)
                else:
                    customer.password=new_password
                    customer.save()
                    new_password=make_password(new_password,hasher='default')
                    user.password=new_password
                    user.save()
                    messages.success(request,'Đã đổi mật khẩu thành công!. Mời quý khách đăng nhập lại.')
                    return redirect("home")
        else:
            messages.error(request,'Sai mật khẩu!')
            return redirect('change_password', id=user.id)
    form =Change_Password_Form()
    return render(request, 'home/change_password.html', {'form':form,'categories':categories})

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page ----------------------------------------------------

#                           -------------------- Customer -----------------------

# Show Customer list
def customer_list(request):
    cusromers = Customer.objects.all()
    paginator = Paginator(cusromers, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/user_manager/customers/customer_list.html', {'page_obj':page_obj})

# add info customer
def add_user(request):
    form=AddCustomerForm()
    if(request.method=="POST"):
        form=AddCustomerForm(request.POST)
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        fullname=request.POST['fullname']
        phone=request.POST['phone']
        address=request.POST['address']
        gender=request.POST['gender']
        if(User.objects.filter(username=username)):
            messages.error(request,'Tên đăng nhập đã tồn tại!')
            return redirect('add_user')
        if(User.objects.filter(email=email)):
            messages.error(request,'Email đã tồn tại!')
            return redirect('add_user')
        if(password!=password2):
             messages.error(request,'Mật khẩu không trùng nhau!')
             return redirect('add_user')
        if(form.is_valid()):
            User.objects.create_user(username,email,password)
            account=Customer(fullname=fullname,phone=phone,username=username,
                             email=email,password=password,address=address,gender=gender)
            account.save()
            messages.success(request,'Thêm khách hàng thành công')
            return redirect('customer_list')
    else:
        form=AddCustomerForm()
    return render(request,'admin/user_manager/customers/add_customer.html',{'form':form})

# Edit customer
def edit_customer_admin(request,id):
    categories=Category.objects.all()
    customer = get_object_or_404(Customer, id=id)
    user=User.objects.filter(username=customer.username).first()
    form =CustomerForm(request.POST,instance=customer)
    if form.is_valid():
        password=request.POST['password']
        password2=request.POST['password2']
        if(password!=password2):
            messages.error(request,'Mật khẩu không trùng nhau!')
            return redirect('edit_customer_admin')
        else:
            form.save()
            password=make_password(password,hasher='default')
            user.password=password
            user.save()
            messages.success(request,'Đã cập nhập khách hàng thành công')
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'admin/user_manager/customers/edit_customer.html', {'form':form,'categories':categories})

# Delete customer 
def delete_customer(request,id):
    customer=Customer.objects.get(id=id)
    account=User.objects.filter(username=customer.username)
    account.delete()
    customer.delete()
    messages.success(request,'Xóa khách hàng thành công')
    return redirect('customer_list')

#                           -------------------- Employee -----------------------

# Show Employee list
def employee_list(request):
    employees = Employee.objects.all()
    paginator = Paginator(employees , 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/user_manager/employees/employee_list.html', {'page_obj':page_obj})

# add Employee
def add_employee(request):
    form=AddEmployeeForm()
    if(request.method=="POST"):
        form=AddEmployeeForm(request.POST)
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        fullname=request.POST['fullname']
        phone=request.POST['phone']
        address=request.POST['address']
        gender=request.POST['gender']
        position=request.POST['position']
        salary=request.POST['salary']
        if(User.objects.filter(username=username)):
            messages.error(request,'Tên đăng nhập đã tồn tại!')
            return redirect('add_employee')
        if(User.objects.filter(email=email)):
            messages.error(request,'Email đã tồn tại!')
            return redirect('add_employee')
        if(password!=password2):
             messages.error(request,'Mật khẩu không trùng nhau!')
             return redirect('add_employee')
        if(form.is_valid()):
            User.objects.create_user(username,email,password)
            account=Employee(username=username,email=email,password=password,fullname=fullname
                             ,phone=phone,address=address,gender=gender,position=position,salary=salary)
            account.save()
            messages.success(request,'Tạo nhân viên thành công')
            return redirect('admin')
    else:
        form=AddEmployeeForm()
    return render(request,'admin/user_manager/employees/add_employee.html',{'form':form})

# Edit employee
def edit_employee(request,id):
    employee = get_object_or_404(Employee, id=id)
    user=User.objects.filter(username=employee.username).first()
    form =EmployeeForm(request.POST,instance=employee)
    if(request.method=="POST"):
        form=EmployeeForm(request.POST)
        old_password=request.POST['old_password']
        password2=request.POST['password2']
        new_password=request.POST['password']
        
        if form.is_valid():
            if(employee.password == old_password):
                if(old_password==new_password):
                    messages.error(request,'Mật khẩu mới không được trùng với mật khẩu cũ!')
                    return redirect('.')
                else:
                    if(new_password!=password2):
                        messages.error(request,'Mật khẩu không trùng nhau!')
                        return redirect('.' )
                    else:
                        form.save()
                        new_password=make_password(new_password,hasher='default')
                        user.password=new_password
                        user.save()
                        messages.success(request,'Đã cập nhập khách hàng thành công')
                        return redirect('edit_employee', id=employee.id)
            else:
                messages.error(request,'Mật khẩu cũ không đúng!')
                return redirect('.')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'admin/user_manager/employees/edit_employee.html', {'form':form})

# Delete employee 
def delete_employee(request,id):
    employee=Employee.objects.get(id=id)
    account=User.objects.filter(username=employee.username)
    account.delete()
    employee.delete()
    messages.success(request,'Xóa nhân viên thành công')
    return redirect('employee_list')

# ------------------------------------------ End Admin Page ----------------------------------------------------

# ------------------------------------------ Begin RestAPI ----------------------------------------------------

# RestAPI Customer
class Customer_API_View(APIView):
    def get(self,request):
        listCustomer=Customer.objects.all()
        Customerdata=CustomerSerializer(listCustomer, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data=Customerdata, status=status.HTTP_200_OK)
    # def post(self,request):
    #     Customerdata=CustomerCreationSerializer(data=request.data)
        
    #     if(not Customerdata.is_valid()):
    #         return Response('Dữ liệu bị sai !', status=status.HTTP_400_BAD_REQUEST)





# ------------------------------------------ End RestAPI ----------------------------------------------------