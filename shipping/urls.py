from django.urls import path
from . import views

urlpatterns = [
    path('update/', views.update_shipping, name='update_shipping'),
]