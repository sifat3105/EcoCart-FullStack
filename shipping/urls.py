from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_shipping, name='update_shipping'),
    path('<str:order_id>/add-update/', views.add_shipping_update, name='add_shipping_update'),
]