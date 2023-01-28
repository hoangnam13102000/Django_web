from django.urls import path
from products import views
urlpatterns = [
# ------------------------------------------ Begin Home Page -------------------------------------------------

#                           -------------------- Product -----------------------

     path('search_products/', views.search_products, name='search_products'),
     path('<int:id>/product_detail/', views.product_view, name='product_detail'),

#                  -------------------- Create Menu Base on Category -----------------------  

     path('<int:category_id>/product_of_category/', views.product_of_category, name='product_of_category'),

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page -------------------------------------------------

#                           -------------------- Category -----------------------

     path('categories/', views.category_list, name='category_list'),
     path('addCategory/' , views.addCategory, name='addCategory'),
     path('<int:id>/edit_category/', views.edit_category, name='edit_category'),
     path('delete/<int:id>', views.delete_category, name='delete_category'),
     
#                           -------------------- Product -----------------------

     path('products/', views.product_list, name='product_list'),
     path('add_product/' , views.add_product, name='add_product'),
     path('<int:id>/edit_product/', views.edit_product, name='edit_product'),
     path('delete_product/<int:id>', views.delete_product, name='delete_product'),
     
#                           -------------------- Comment -----------------------

     path('comment_list/', views.comment_list, name='comment_list'),
     path('<int:comment_id>/delete_comment', views.delete_comment, name='delete_comment'),

# ------------------------------------------ End Admin Page ----------------------------------------------------
     
]