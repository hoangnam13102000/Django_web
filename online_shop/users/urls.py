from django.urls import path
from users import views

urlpatterns = [
# ------------------------------------------ Begin Home Page -------------------------------------------------

#                           -------------------- Customer -----------------------
     path('<int:id>/edit_info/' , views.edit_info, name='edit_info'),
     path('<int:id>/change_password/' , views.change_password, name='change_password'),

# ------------------------------------------ End Home Page ----------------------------------------------------

# ------------------------------------------ Begin Admin Page -------------------------------------------------

#                           -------------------- Customer -----------------------
     path('customer_list/' , views.customer_list, name='customer_list'),
     path('add_user/' , views.add_user, name='add_user'),
     path('<int:id>/edit_customer_admin/' , views.edit_customer_admin, name='edit_customer_admin'),
     path('<int:id>/delete_customer/' , views.delete_customer, name='delete_customer'),
     path('search_customer/' , views.search_customer, name='search_customer'),

#                           -------------------- Employee -----------------------

     path('employee_list/' , views.employee_list, name='employee_list'),
     path('add_employee/' , views.add_employee, name='add_employee'),
     path('<int:id>/edit_employee/' , views.edit_employee, name='edit_employee'),
     path('<int:id>/delete_employee/' , views.delete_employee, name='delete_employee'),
     path('search_employee/' , views.search_employee, name='search_employee'),
     path('<int:id>/profile_employee/' , views.profile_employee, name='profile_employee'),

# ------------------------------------------ End Admin Page ----------------------------------------------------
]