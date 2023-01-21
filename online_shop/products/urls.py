from django.urls import path
from products import views
urlpatterns = [
     path('categories/', views.category_list, name='category_list'),
     path('addCategory/' , views.addCategory, name='addCategory'),
     path('delete/<int:id>', views.delete_category, name='delete_category'),
     path('<int:id>/edit_category/', views.edit_category, name='edit_category'),
     path('products/', views.product_list, name='product_list'),
     path('add_product/' , views.add_product, name='add_product'),
     path('delete_product/<int:id>', views.delete_product, name='delete_product'),
     path('<int:id>/edit_product/', views.edit_product, name='edit_product'),
     path('<int:id>/product_detail/', views.product_view, name='product_detail'),
     path('<int:category_id>/product_of_category/', views.product_of_category, name='product_of_category'),
     path('search_products/', views.search_products, name='search_products'),
     path('comment_list/', views.comment_list, name='comment_list'),
     path('<int:comment_id>/delete_comment', views.delete_comment, name='delete_comment'),
]