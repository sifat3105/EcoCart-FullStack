from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_views, name='home'),
    path('quick-view/<slug:product_slug>/', views.quick_view, name='quick_view'),
    path('load-more/', views.load_more, name='load_more'),
]
