from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'customer_name', 'shipping_address','phone_number', 'payment_method'
        ]
        choices_payment=(('Tiền mặt','Tiền mặt'),('Chuyển khoản','Chuyển khoản'))
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Tên khách hàng'}),
            'shipping_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Địa chỉ giao hàng'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Số điện thoại'}),
            'payment_method': forms.Select(choices=choices_payment,attrs={'class': 'form-control'}),
        }