from django.urls import path
from .views import create_product_views, product_detail, product_list_view, search_redirect, product_search

urlpatterns = [
    path('seller/producct/create/', create_product_views, name='create_product'),
    path('product/<slug:product_slug>/', product_detail, name='product'),
    # path('', product_list_view, name='products'),
    path('search/', search_redirect, name='search_redirect'), 
    path('catalog/', product_search, name='product_search'),
]