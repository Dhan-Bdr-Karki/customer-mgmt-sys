from django.contrib import admin
from django.urls import path
from . import views

# Adding in user password reset email using django's built in authentication class & authentication views.
from django.contrib.auth import views as auth_view



urlpatterns = [
    path('',views.home, name="home"),

    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user-page/', views.userPage, name='user-page'),

    # for account profile
    path('account/', views.accountSettings, name="account"),


    path('products/',views.products, name="products"),
    path('add-product/',views.addProduct, name="add-product"),

    path('create-customer/',views.addCustomer, name="create-customer"),
    path('customer/<str:pk_test>/',views.customer, name="customer"),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('remove_order/<str:pk>/', views.deleteOrder, name="remove_order"),


# password reset email

    # 1. Submit email form
    path('reset_password/', 
    auth_view.PasswordResetView.as_view(template_name = "accounts/password_reset.html" ), 
    name = 'reset_password'),

    # Email sent success message
    path('reset_password_sent/',
    auth_view.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html" ),
    name = 'password_reset_done'),

    # Link to password reset form in email
    path('reset/<uidb64>/<token>', 
    auth_view.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), 
    name='password_reset_confirm'),

    # Password successfully changed messages
    path('reset_password_complete/', 
    auth_view.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"), 
    name='password_reset_complete'),
]