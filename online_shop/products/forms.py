from django import forms
from . models import Category,Comment,Product

# Form Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image', 'title', 'category', 'price', 'description','is_active','brand']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control',"type":"file"}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tên sản phẩm'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Gía sản phẩm'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Mô tả sản phẩm'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Hãng'}),
        }
        
# Form Category
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Loại sản phẩm'})
        }

# Form Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('commenter_name','commenter_email','comment_body')
        widgets = {
            'commenter_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nhập tên','required':''}),
            'commenter_email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email','required':''}),
            'comment_body': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nhận xét','required':''}),
        }