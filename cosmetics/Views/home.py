from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from app.models.banner import Banner
from app.models.category import Category
from app.models.offers import Offers
from app.models.product import Product, Product_Image
from .add_to_cart import Add_to_wishlist, Add_to_Cart, Increment_to_Cart, decrement_to_Cart
from django.contrib import messages


class Home(View):

    def get(self, request):
        
        #banner fetch
        banners = Banner.objects.all()
        #categories fetch
        categorys = Category.objects.all()
        #product fetch
        products = Product.objects.all()
        #offers fetch
        offers = Offers.objects.all()
        #Get Quick View
        quick_view = request.GET.get('quick_view')
        del_session = request.GET.get('del_session')
        
        if del_session:
            del request.session['quick_view']
            return redirect('home')

        if quick_view:
            request.session['quick_view'] = quick_view 
            print(quick_view)

        if request.session.get('quick_view'):
            quick_view = request.session.get('quick_view')
            quick_view_product = Product.objects.get(id=quick_view)
            quick_view_images = Product_Image.objects.filter(product__id=quick_view).first()
            print(request.session.get('quick_view'))
            data={
            'banners':banners[::-1][:4],
            'category': categorys[:6],
            'products':products,
            'offers':offers,
            'quick_view_product':quick_view_product,
            'quick_view_image':quick_view_images,
            }

            return render(request, 'index.html', data)
        
        
        data={
            'banners':banners[::-1][:4],
            'category': categorys[:6],
            'products':products,
            'offers':offers,
        }

        return render(request, 'index.html', data)
    

    def post(self, request):

        wishlist_id = request.POST.get('wish_id')
        cart_id = request.POST.get('add_cart_id')

        add_id = request.POST.get('add_id')
        minus_id = request.POST.get('minus_id')

        if add_id:
            response_message = Increment_to_Cart(request, add_id)
            return redirect('home')
        if minus_id:
            response_message = decrement_to_Cart(request,minus_id)
            return redirect('home')
        
        if wishlist_id:
            response_message = Add_to_wishlist(request, wishlist_id)
            messages.success(request, response_message)
            return redirect('home')
        
        if cart_id:
            response_message = Add_to_Cart(request, cart_id)
            messages.success(request, response_message)
            return redirect('home')
        
        return redirect('home')
