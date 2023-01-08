from django.urls import path
from order import views
urlpatterns = [
    path('mycart/' , views.cart, name='cart'),
    path('<int:product_id>/add_to_cart/', views.add_to_cart, name = 'add_to_cart'),
    path('clear_cart/' , views.clear_cart, name='clear_cart'),
    path('<int:product_id>/remove_from_cart/', views.remove_from_cart, name = 'remove_from_cart'),
    path('checkout/', views.checkout, name = 'checkout'),
    path('order_list/', views.order_list, name = 'order_list'),
    path('<int:order_id>/delete_order/', views.delete_order, name = 'delete_order'),
]