from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('shipping/', include('shipping.urls')),
    path('checkout/', include('checkout.urls')),
    # path('order/', include('order.urls')),
    # path('review/', include('review.urls')),
    path('discounts/', include('discounts.urls')),
    # path('payment/', include('payment.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)