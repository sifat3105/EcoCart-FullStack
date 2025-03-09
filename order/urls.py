from django.urls import path
from . import views
urlpatterns = [
    path('order/details/', views.order_details, name='order-details'),
    path('track/order/', views.tack_order, name='track-order')
]
