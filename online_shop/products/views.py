from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import  Category,Product,Comment
from . forms import CategoryForm,ProductForm,CommentForm
from . utils import handle_upload_file
# Create your views here.

# View Product in home page
def product_view(request, id):
    product = get_object_or_404(Product, pk=id)
    categories=Category.objects.all()
    comments= product.comments.all()
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.product = product
                comment.save()
                return redirect('product_detail', id)     
        else:
            messages.error(request,'Bạn cần đăng nhập để bình luận!')
    form = CommentForm()
    return render(request, 'home/product_detail.html',{'product': product,'categories':categories, 'form': form,'comments':comments})

# Show list Product admin
def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/product_manager/list_product.html', {'page_obj': page_obj})

# Show list Comment admin
def comment_list(request):
    comments = Comment.objects.all()
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/comment_manager/comment_list.html', {'page_obj': page_obj})

# Delete comment
def delete_comment(request, comment_id):
    # get id comment 
    comment = Comment.objects.get(id=comment_id)
    # Delete comment
    comment.delete()
    messages.success(request,'Xóa bình luận thành công')
    return redirect('comment_list')

# Add product in list
def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            handle_upload_file(request.FILES['image'])
            product = form.save(commit=False)
            product.category = form.cleaned_data['category']
            product.save()
            messages.success(request,'Thêm sản phẩm thành công')
            return redirect('product_list')
        else:
            messages.error(request,'Thêm sản phẩm thất bại')
    else:
        form = ProductForm()
    return render(request, 'admin/product_manager/add_product.html', {'form':form})

# Edit product
def edit_product(request,id):
    product = get_object_or_404(Product, id=id)
    form =ProductForm(request.POST, request.FILES,instance=product)
    if form.is_valid():
        handle_upload_file(request.FILES['image'])
        form.save()
        messages.success(request,'Đã cập nhập sản phẩm thành công')
        return redirect("edit_product", id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_manager/edit_product.html', {'form': form})

# Delete product
def delete_product(request, id):
    # get id product 
    product = Product.objects.get(id=id)
    # Delete product
    product.delete()
    messages.success(request,'Xóa sản phẩm thành công')
    return redirect('product_list')

# Search product
def search_products(request):
    query = request.GET.get('query')
    data = Product.objects.filter(title__icontains=query).order_by('-id')
    categories=Category.objects.all()
    return render(request, 'home/search.html', {'data': data,'categories':categories})

# Show Category list
def category_list(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/category_manager/category_list.html', {'page_obj': page_obj})

#Form add Category
def addCategory(request):
    form=CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        name=request.POST['name']
        if(Category.objects.filter(name=name)):
            messages.error(request,'Loại sản phẩm đã tồn tại!')
            return redirect('addCategory')
        if form.is_valid():
            form.save()
            messages.success(request,'Thêm loại sản phẩm thành công')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'admin/category_manager/add_category.html', {'form':form})

# Edit Category by id
def edit_category(request,id):
    category=get_object_or_404(Category, id=id)
    form =CategoryForm(request.POST,instance=category)
    if form.is_valid():
        form.save()
        messages.success(request,'Cập nhập thông tin thành công')
        return redirect("edit_category",id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/category_manager/edit_category.html', {'form': form})

# Delete Category by id
def delete_category(request, id):
    # get id category 
    category = Category.objects.get(id=id)
    # Delete category
    category.delete()
    messages.success(request,'Xóa loại sản phẩm thành công')
    return redirect('category_list')

# Show product depend on category
def product_of_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories=Category.objects.all()
    product=Product.objects.filter(category=category).all()
    paginator = Paginator(product, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/shop_product_list.html', {'page_obj':page_obj,'categories':categories,'category':category})



