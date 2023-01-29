from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from users.models import Employee
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import  Category,Product,Comment
from . forms import CategoryForm,ProductForm,CommentForm, SearchProductForm, SearchCommentForm
from . utils import handle_upload_file
from .serializers import ProductSerializer,CategorySerializer,CommentSerializer #,CustomerCreationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

# ------------------------------------------ Begin Home Page ----------------------------------------------------

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

# Show product depend on category
def product_of_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    categories=Category.objects.all()
    product=Product.objects.filter(category=category).all()
    paginator = Paginator(product, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/shop_product_list.html', {'page_obj':page_obj,'categories':categories,'category':category})

# Search product
def search_products(request):
    keyword = request.GET.get('keyword')
    data = Product.objects.filter(title__icontains=keyword).order_by('-id')
    categories=Category.objects.all()
    return render(request, 'home/search.html', {'data': data,'categories':categories})

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page ----------------------------------------------------


# Show list Product admin
def product_list(request):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    search_form= SearchProductForm()
    products = Product.objects.all()
    paginator = Paginator(products, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/product_manager/products/list_product.html', {'page_obj': page_obj,'employee':employee,'search_form':search_form})


# Add product into list
def add_product(request):
    form = ProductForm()
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
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
    return render(request, 'admin/product_manager/products/add_product.html', {'form':form,'employee':employee})

# Edit product
def edit_product(request,id):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    product = get_object_or_404(Product, id=id)
    form =ProductForm(request.POST, request.FILES,instance=product)
    if form.is_valid():
        handle_upload_file(request.FILES['image'])
        form.save()
        messages.success(request,'Đã cập nhập sản phẩm thành công')
        return redirect("edit_product", id=product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_manager/products/edit_product.html', {'form': form,'employee':employee, 'product':product})

# Delete product
def delete_product(request, id):
    # get id product 
    product = Product.objects.get(id=id)
    # Delete product
    product.delete()
    messages.success(request,'Xóa sản phẩm thành công')
    return redirect('product_list')

# Search product admin
def search_product_admin(request):
    search_type=request.GET.get('search_type')
    keyword = request.GET.get('keyword')
    search_form= SearchProductForm()
    if search_type == "Thương hiệu":
        data = Product.objects.filter(brand__icontains=keyword).order_by('-id')
    else:
        data = Product.objects.filter(title__icontains=keyword).order_by('-id')
    return render(request, 'admin/product_manager/products/search_product.html', {'data':data ,'search_form':search_form})

#                           -------------------- Category -----------------------

# Show Category list
def category_list(request):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    categories = Category.objects.all()
    paginator = Paginator(categories, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/product_manager/categories/category_list.html', {'page_obj': page_obj,'employee':employee})

#Form add Category
def addCategory(request):
    form=CategoryForm()
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
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
    return render(request, 'admin/product_manager/categories/add_category.html', {'form':form,'employee':employee})

# Edit Category by id
def edit_category(request,id):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    category=get_object_or_404(Category, id=id)
    form =CategoryForm(request.POST,instance=category)
    if form.is_valid():
        form.save()
        messages.success(request,'Cập nhập thông tin thành công')
        return redirect("edit_category",id=category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/product_manager/categories/edit_category.html', {'form': form,'employee':employee,'category':category})

# Delete Category by id
def delete_category(request, id):
    # get id category 
    category = Category.objects.get(id=id)
    # Delete category
    category.delete()
    messages.success(request,'Xóa loại sản phẩm thành công')
    return redirect('category_list')

# Search Category
def search_category(request):
    keyword = request.GET.get('keyword')
    data = Category.objects.filter(name__icontains=keyword).order_by('-id')
    return render(request, 'admin/product_manager/categories/search_category.html', {'data':data })

#                           -------------------- Comment -----------------------

# Show list Comment admin
def comment_list(request):
    user=request.user
    employee =Employee.objects.filter(username=user.username).first()
    search_form= SearchCommentForm()
    comments = Comment.objects.all()
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/product_manager/comments/comment_list.html', {'page_obj': page_obj,'employee':employee,'search_form':search_form})

# Delete comment
def delete_comment(request, comment_id):
    # get id comment 
    comment = Comment.objects.get(id=comment_id)
    # Delete comment
    comment.delete()
    messages.success(request,'Xóa bình luận thành công')
    return redirect('comment_list')

def search_comment(request):
    search_type=request.GET.get('search_type')
    keyword = request.GET.get('keyword')
    search_form= SearchCommentForm()
    if search_type == "Email":
        data = Comment.objects.filter(commenter_email__icontains=keyword).order_by('-id')
    else:
        data = Comment.objects.filter(commenter_name__icontains=keyword).order_by('-id')
    return render(request, 'admin/product_manager/comments/search_comment.html', {'data':data ,'search_form':search_form})

# ------------------------------------------ End Admin Page ----------------------------------------------------


# ------------------------------------------ Begin RestAPI ----------------------------------------------------

#                           -------------------- Product -----------------------

# RestAPI  Product
class Product_API_View(APIView):
    def get(self,request):
        listProduct= Product.objects.all()
        Productdata= ProductSerializer(listProduct, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data= Productdata, status=status.HTTP_200_OK)
    # def post(self,request):
    #    Productdata=ProductCreationSerializer(data=request.data)
        
    #     if(not Productdata.is_valid()):
    #         return Response('Dữ liệu bị sai !', status=status.HTTP_400_BAD_REQUEST)

#                           -------------------- Category -----------------------

# RestAPI Category
class  Category_API_View(APIView):
    def get(self,request):
        listCategory= Category.objects.all()
        Categorydata= CategorySerializer(listCategory, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data= Categorydata, status=status.HTTP_200_OK)

#                           -------------------- Product -----------------------

# RestAPI Comment
class  Comment_API_View(APIView):
    def get(self,request):
        listComment= Comment.objects.all()
        Commentdata= CommentSerializer(listComment, many=True).data # Adding .data to convert the data from ListSerializer to JSON
        return Response(data= Commentdata, status=status.HTTP_200_OK)
    
# ------------------------------------------ End RestAPI ----------------------------------------------------