from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_views, name='home'),
    path('load-more/', views.load_more, name='load_more'),
    path('test/', views.test)
]
