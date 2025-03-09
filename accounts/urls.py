from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('seller/register/', views.seller_registration_view, name='seller_registration'),
    path('seller/verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('seller/login/', views.seller_login_view, name='seller-login'),
    path('seller/logout/', views.seller_logout, name='seller_logout'),
    path('seller/dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    path('register/', views.customer_register, name='register'),
    path('authentication/', views.customer_login, name='authentication'),
    path('auth_reverse/', views.auth_reverse, name='auth_reverse'),
    path('', views.account_views, name='my-account'),
    path('logout/', views.customer_logout, name='logout'),
]
