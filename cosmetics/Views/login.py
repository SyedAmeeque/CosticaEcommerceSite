from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib import messages
from app.models.product import Product
from app.models.cart import Cart
from app.models.wishlist import Wishlist
from app.models.cart_item import Cart_item
from app.models.wish_item import Wish_item

class Login(View):

    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        
        if request.session.get('cart') and user is not None:
            cart = request.session.get('cart')
            keys = list(cart.keys())
            products = Product.objects.filter(id__in=keys)
            cart, created = Cart.objects.get_or_create(user=user)
            for p in products:
                quantity = request.session.get('cart').get(str(p.id))
                total_price = p.sale_price * quantity
                filter_cart_item = Cart_item.objects.filter(cart=cart, product=p).first()
                if filter_cart_item:
                    filter_cart_item.quantity = quantity
                    filter_cart_item.total_price = filter_cart_item.product.sale_price * quantity
                    filter_cart_item.save()
                else:   
                    cart_item = Cart_item.objects.create(cart=cart, product=p, quantity=quantity, total_price=total_price)
            del request.session['cart']
        
        if request.session.get('wishlist') and user is not None:
            wishlist = request.session.get('wishlist')
            keys = list(wishlist.keys())
            products = Product.objects.filter(id__in=keys)
            wishlist, created = Wishlist.objects.get_or_create(user=user)
            for p in products:
                wish_item, created_item = Wish_item.objects.get_or_create(wish=wishlist, product=p)
            del request.session['wishlist']
            
                


        if user is not None:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('home')  # Redirect to a home or dashboard page
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')

        
        
        return render(request, 'login.html')
