from django.urls import path
from . import views

urlpatterns = [
    path('apply/coupon/<int:cart_id>/<str:coupon_code>/', views.coupon_apply, name='coupon-apply')
]