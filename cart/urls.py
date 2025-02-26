from django.urls import path
from . import views

urlpatterns = [
    path('add-to-cart/<slug:product_slug>/<int:num_product>/', views.add_to_cart, name='add_to_cart'),
    path('', views.cart_view, name='cart'),

]
