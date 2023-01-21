from django import forms
from .models import Contact

# Form Contact
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('customer_name','customer_email','content')
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nhập tên','required':''}),
            'customer_email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email','required':''}),
            'content': forms.TextInput(attrs={'class': 'form-control','placeholder':'Đừng ngại hỏi về đơn hàng của bạn','required':''}),
        }