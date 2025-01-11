from django.shortcuts import render, redirect
from django.views import View
from app.models.category import Category
from app.models.wishlist import Wishlist
from app.models.product import Product, Product_Image
from django.db.models import Q
from .add_to_cart import Add_to_Cart, Add_to_wishlist, Increment_to_Cart, decrement_to_Cart
from django.contrib import messages
# Create your views here.

class Searching(View):

    def get(self, request):

      


      
        search = request.GET.get('search_query')
        category_id = request.GET.get('category')
        categorys = Category.objects.all()
        message = 'Search Results For You'
       
        if category_id:
            products = Product.objects.filter(category__in=category_id)
        elif search:
            products = Product.objects.filter( 
                    Q(title__icontains=search) |
                    Q(excerpt__icontains=search) |
                    Q(description__icontains=search) |
                    Q(product_type__name__icontains=search) |
                    Q(brand__brand__icontains=search)
                    )
        else:
            message = "No Search Query"
       
        if len(products) == 0:
            message = "Result Not Found"

            
        #Get Quick View
        quick_view = request.GET.get('quick_view')
        del_session = request.GET.get('del_session')
        
        if del_session:
            del request.session['quick_view']
            return redirect('search')

        if quick_view:
            request.session['quick_view'] = quick_view 
            print(quick_view)

        if request.session.get('quick_view'):
            quick_view = request.session.get('quick_view')
            quick_view_product = Product.objects.get(id=quick_view)
            quick_view_images = Product_Image.objects.filter(product__id=quick_view).first()
            print(request.session.get('quick_view'))
            data={
                'message':message,
                'products':products,
                'quick_view_product':quick_view_product,
                'quick_view_image':quick_view_images,
            }
            return render(request, 'searching.html', data)


        data={
            'category':categorys,
            'products':products,
            'message':message,

        }
        return render(request, 'searching.html', data)
    
    def post(self, request):

        wishlist_id = request.POST.get('wish_id')
        cart_id = request.POST.get('add_cart_id')

        add_id = request.POST.get('add_id')
        minus_id = request.POST.get('minus_id')

        if add_id:
            response_message = Increment_to_Cart(request, add_id)
            return redirect('search')
        
        if minus_id:
            response_message = decrement_to_Cart(request, minus_id)
            return redirect('search')

        if wishlist_id:
            response_message = Add_to_wishlist(request, wishlist_id)
            messages.success(request, response_message)
            return redirect('search')
        
        if cart_id:
            response_message = Add_to_Cart(request, cart_id)
            messages.success(request, response_message)
            return redirect('search')
        
        return redirect('search')