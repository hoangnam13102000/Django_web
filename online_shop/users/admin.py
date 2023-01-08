from django.contrib import admin
from .models import Customer

class CustomerAdmin(admin.ModelAdmin):
    list_display =('id','fullname','gender','address','phone','username','password','email')
admin.site.register(Customer,CustomerAdmin)