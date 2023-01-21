from django.urls import path
from users import views
urlpatterns = [
     path('customer_list/' , views.customer_list, name='customer_list'),
     path('add_user/' , views.add_user, name='add_user'),
     path('<int:id>/delete_customer/' , views.delete_customer, name='delete_customer'),
     path('<int:id>/edit_customer_admin/' , views.edit_customer_admin, name='edit_customer_admin'),
     path('<int:id>/edit_info/' , views.edit_info, name='edit_info'),
     path('<int:id>/change_password/' , views.change_password, name='change_password'),
     
]