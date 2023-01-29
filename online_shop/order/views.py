from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from users.models import Customer,Employee
from django.contrib import messages
from .forms import OrderForm,SearchOrderForm
from .models import Order
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from products.models import  Category
from .serializers import OrderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# ------------------------------------------ Begin Home Page ----------------------------------------------------

# Add Product Into Cart 
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id) # get id product will be adđe cart
    if 'cart' not in request.session: # check cart is existing
         request.session['cart'] = [] # initialization cart
    item_index = -1
    for i, item in enumerate(request.session['cart']): # check product already existsin cart
        if item['id'] == product_id:
            item_index = i
            break
    if item_index >= 0:
        request.session['cart'][item_index]['quantity'] += 1
    else:
        request.session['cart'].append({
            'id': product_id,
            'image':product.image.url,
            'name': product.title,
            'description':product.description,
            'price': product.price,
            'quantity': 1,
        })
    request.session.modified = True
    return redirect('cart')

# View Cart
def cart(request):
    cart_items = []
    total = 0
    if 'cart' in request.session:
        for item in request.session['cart']:
            # product = get_object_or_404(Product, pk=item['id'])
            item['total_price'] = item['price'] * item['quantity']
            total += item['total_price']
            cart_items.append(item)
    form = OrderForm()
    categories=Category.objects.all()
    return render(request, 'home/view_cart.html', {'cart_items': cart_items, 'total': total, 'form':form,'categories':categories})


# Clear Cart
def clear_cart(request):
    if request.session['cart']:
        del request.session['cart']
        messages.success(request,'Xóa giỏ hàng thành công')
    else:
        messages.error(request,'Bạn chưa có sản phẩm nào trong giỏ hàng')
        return redirect('home')
    return redirect('cart')

# Delete item from cart
def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        for i, item in enumerate(request.session['cart']):
            if item['id'] == product_id:
                request.session['cart'].pop(i)
                break
    request.session.modified = True
    return redirect('cart')

# Check out the product
def checkout(request):
    categories=Category.objects.all() 
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            customer_name=request.POST['customer_name']
            user_id= request.user.id
            user = get_object_or_404(User, id=user_id)
            customer = Customer.objects.filter(id=user.id).first()
            shipping_address=request.POST['shipping_address']
            phone_number=request.POST['phone_number']
            payment_method=request.POST['payment_method']
            if form.is_valid():
                order = form.save(commit=False)
                cart_items = request.session['cart']
                # total = 0
                for item in cart_items:
                    product = get_object_or_404(Product, pk=item['id'])
                    order = Order(customer_name=customer_name,product=product, shipping_address= shipping_address 
                                ,quantity=item['quantity'], total_price=item['price'],phone_number=phone_number,payment_method=payment_method,customer =customer  )
                    order.save()
                    # total += item['total_price']
                    # order.total_price = total
                    # order.save()
                    request.session['cart'] = []
            messages.success(request,'Bạn đã đặt hàng thành công')
            return redirect('cart')
    else:
        messages.error(request,'Bạn phải đăng nhập trước khi thanh toán')
        form = OrderForm()
    return render(request, 'home/view_cart.html', {'form':form,'categories':categories})

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page ----------------------------------------------------

# Show Order list
def order_list(request):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    search_form= SearchOrderForm()
    order = Order.objects.all()
    paginator = Paginator(order, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/orders_manager/order_list.html', {'page_obj':page_obj,'employee':employee,'search_form':search_form})

# Delete order 
def delete_order(request,order_id):
    order=Order.objects.get(id=order_id)
    order.delete()
    messages.success(request,'Xóa đơn đặt hàng thành công')
    return redirect('order_list')

# Search Order
def search_order(request):
    search_type=request.GET.get('search_type')
    keyword = request.GET.get('keyword')
    search_form= SearchOrderForm()
    if search_type == "Địa chỉ":
        data = Order.objects.filter(shipping_address__icontains=keyword).order_by('-id')
    elif search_type == "Số điện thoại":
        data = Order.objects.filter(phone_number__icontains=keyword).order_by('-id')
    else:
        data = Order.objects.filter(customer_name__icontains=keyword).order_by('-id')
    return render(request, 'admin/orders_manager/search_order.html', {'data':data ,'search_form':search_form})

# ------------------------------------------ End Admin Page ----------------------------------------------------

# ------------------------------------------ Begin RestAPI ----------------------------------------------------

# RestAPI Order
class  Order_API_View(APIView):
    def get(self,request):
        listOrder= Order.objects.all()
        Orderdata= OrderSerializer(listOrder, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data= Orderdata, status=status.HTTP_200_OK)

# ------------------------------------------ End RestAPI ----------------------------------------------------