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
    path('view_cart', views.view_cart),
    path('profile', views.profile),
    path('address', views.address),
    path('view_address', views.viewaddress),
    path('update/<str:address_id>', views.editaddress),
    path('remove/<str:address_id>', views.remove),
    path('review/<str:product_id>', views.addreview),
    path('removes/<str:cart_id>', views.removes),
    path('wishlist', views.wishlist),
    path('search', views.search),
    path('about', views.about),
    # path('otp/<uid>',otp)

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

