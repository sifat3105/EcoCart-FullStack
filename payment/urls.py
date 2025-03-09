from django.urls import path
from . import views

urlpatterns = [
    path('sslcommerz/', views.sslcommerz_payment, name="sslcommerz_payment"),
    path('retry/sslcommerz/', views.sslcommerz_retry_payment, name="sslcommerz_retry_payment"),
    path('cash-on-delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('fail/', views.payment_fail, name='payment_fail'),
    path('cancel/', views.payment_cancel, name='payment_cancel'),
    path('success/', views.payment_success, name='payment_success'),
    path('cash-on-delivery/success/', views.payment_success, name='payment_success'),

]