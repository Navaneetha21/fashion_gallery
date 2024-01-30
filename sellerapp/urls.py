from django.urls import path
from sellerapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('seller_login',views.seller_login),
    path('seller_register',views.seller_register),
    path('add_product',views.add_product),
    path('view_producttable', views.viewpdct),
    path('update/<str:product_id>', views.edit),
    path('remove/<str:product_id>', views.remove),
    path('image/<str:product_id>', views.image, name='image'),
    path('seller_page', views.seller_home),
    path('seller_logout', views.seller_logout, name='seller_logout'),
    path('product', views.product)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)