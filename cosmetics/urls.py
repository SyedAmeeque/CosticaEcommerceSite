"""
URL configuration for cosmetics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .Views import home,cart, products,signup,login,shop,wishlist, logout, searching, checkout, orders, contact, about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.Home.as_view(), name='home'),   
    path('cart/', cart.Cart.as_view(), name='cart'),   
    path('signup/', signup.Signup.as_view(), name='signup'),   
    path('login/', login.Login.as_view(), name='login'),   
    path('shop/', shop.Shop.as_view(), name='shop'),   
    path('wishlist/', wishlist.Wishlist.as_view(), name='wishlist'),   
    path('product/<str:slug>/', products.Product_View.as_view(), name='product'),   
    path('logout/', logout.Logout.as_view(), name='logout'),   
    path('searching/', searching.Searching.as_view(), name='search'),   
    path('checkout/', checkout.Checkout.as_view(), name='checkout'),   
    path('orders/', orders.Orders.as_view(), name='orders'),   
    path('contact-us/', contact.Contact.as_view(), name='contact'),   
    path('about-us/', about.About.as_view(), name='about'),   
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)