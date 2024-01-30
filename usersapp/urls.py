from django.urls import path
from usersapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('user_login',views.user_login),
    path('user_register',views.user_register),
    path('',views.home),
    path('logout', views.logout, name='logout'),
    path('view_product/<str:id>', views.view_product, name='view_product'),
    path('view_product/view_cart/<str:id>', views.view_cart, name='view_cart'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

