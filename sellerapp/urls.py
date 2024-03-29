from django.urls import path
from sellerapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('seller_login',views.seller_login),
    path('seller_register',views.seller_register),
    path('add_product',views.add_product),
    path('view_producttable', views.viewpdct),
    path('update/<str:product_id>', views.editproduct),
    path('remove/<str:product_id>', views.remove),
    path('image_page/<str:product_id>', views.image_page, name='image_page'),
    path('view_offer', views.viewoffer),
    path('add_offer/<str:product_id>', views.addoffer, name='addoffer'),
    path('update_offer/<str:offer_id>', views.update_offer),
    path('remove_offer/<str:offer_id>', views.remove_offer),
    path('seller_page', views.seller_home),
    path('seller_logout', views.seller_logout, name='seller_logout'),
    path('product', views.product),
    path('addproduct_page', views.addprdct),
    path('viewproduct_page', views.viewproduct),
    path('seller_order', views.seller_order),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)