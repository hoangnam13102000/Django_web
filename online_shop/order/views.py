from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from users.models import Customer
from django.contrib import messages
from .forms import OrderForm
from .models import Order
from django.core.paginator import Paginator

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
    return render(request, 'home/view_cart.html', {'cart_items': cart_items, 'total': total, 'form':form})


# Clear Cart
def clear_cart(request):
    if request.session['cart']:
        del request.session['cart']
        messages.success(request,'Xóa giỏ hàng thành công')
    else:
        messages.error(request,'Bạn chưa có sản phẩm nào trong giỏ hàng')
        return redirect('home')
    return redirect('cart')

def remove_from_cart(request, product_id):
    if 'cart' in request.session:
        for i, item in enumerate(request.session['cart']):
            if item['id'] == product_id:
                request.session['cart'].pop(i)
                break
    request.session.modified = True
    return redirect('cart')

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        customer_name=request.POST['customer_name']
        customer = Customer.objects.filter(fullname=customer_name).first()
        shipping_address=request.POST['shipping_address']
        phone_number=request.POST['phone_number']
        payment_method=request.POST['payment_method']
        if form.is_valid():
            order = form.save(commit=False)
            cart_items = request.session['cart']
            total = 0
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
        form = OrderForm()
    return render(request, 'home/view_cart.html', {'form': form})

# Show Order list
def order_list(request):
    order = Order.objects.all()
    paginator = Paginator(order, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/orders_manager/order_list.html', {'page_obj':page_obj})

# Delete order 
def delete_order(request,order_id):
    order=Order.objects.get(id=order_id)
    order.delete()
    messages.success(request,'Xóa đơn đặt hàng thành công')
    return redirect('order_list')