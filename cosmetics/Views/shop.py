from django.shortcuts import render, redirect
from django.views import View
from app.models.category import Category
from app.models.wishlist import Wishlist
from app.models.product import Product, Product_Image
from django.db.models import Q
from .add_to_cart import Add_to_Cart, Add_to_wishlist, Increment_to_Cart, decrement_to_Cart
from django.contrib import messages
from decimal import Decimal
# Create your views here.

class Shop(View):

    def get(self, request):

        category_session_del = request.GET.get('del_category_session')
        search_session_del = request.GET.get('del_search_session')
        rating_session_del = request.GET.get('del_rating_session')
        pricing_session_del = request.GET.get('del_pricing_session')

        
        
        if category_session_del:
            del request.session['category_query']
            return redirect('shop')

        if search_session_del:
            del request.session['search_query']
            return redirect('shop')
        
        if rating_session_del:
            del request.session['rating_search']
            return redirect('shop')

        if pricing_session_del:
            del request.session['min']
            del request.session['max']
            return redirect('shop')
       
        
    

        category_id = request.GET.get('category')
        search = request.GET.get('main_search')
        order_by = request.GET.get('order_by')
        rating = request.GET.get('rating')
        min = request.GET.get('min')
        max = request.GET.get('max')

         
        products = Product.objects.all()
        categorys = Category.objects.all()
       # Initialize session variables
        if request.session.get('search_query'):
            search_session = request.session['search_query']
        else:
            search_session = None
        if request.session.get('category_query'):
            category_session = request.session.get('category_query')
        else:
            category_session = None
        if request.session.get('order_by_query'):
            order_by_session = request.session.get('order_by_query')
        else:
            order_by_session = None
        if request.session.get('rating_search'):
            rating_session = request.session.get('rating_search')
        else:
            rating_session = None
        if request.session.get('min') and request.session.get('max'):
            min_price_session = request.session.get('min')
            max_price_session = request.session.get('max')
        else:
            max_price_session = None
            min_price_session = None

        if rating:
            request.session['rating_search'] = rating
            rating_session = rating
        # Store search query in session if provided
        if search:
            request.session['search_query'] = search
            search_session = search

        # Store category ID in session if provided
        if category_id:
            request.session['category_query'] = category_id
            category_session = category_id

        # Store order_by in session if provided
        if order_by:
            request.session['order_by_query'] = order_by
            order_by_session = order_by

        if min and max:
            request.session['min'] = min
            request.session['max'] = max
            max_price_session = max
            min_price_session = min

      


        if search_session or category_session or rating_session or (max_price_session and min_price_session):
            products = products.none()

            filters = Q()  # Start with an empty Q object

            if search_session:
                search_filter = (
                    Q(title__icontains=search_session) |
                    Q(excerpt__icontains=search_session) |
                    Q(description__icontains=search_session) |
                    Q(category__name__icontains=search_session)
                )
                products = products.union(Product.objects.filter(search_filter))  # Add to the result

            if category_session:
                category_filter = Q(category__in=category_session)
                products = products.union(Product.objects.filter(category_filter))  # Add to the result
            
            if rating_session:
                rating_filter = Q(product_reviews__gte=rating_session) & Q(product_reviews__lte=5.0)
                products = products.union(Product.objects.filter(rating_filter))  
            
            if max_price_session and min_price_session:
                pricing_filter = Q(sale_price__gte=Decimal(min_price_session)) & Q(sale_price__lte=Decimal(max_price_session))
                products = products.union(Product.objects.filter(pricing_filter))  
                print(products)
        
        # Apply ordering based on session variable
        if order_by_session:
            if order_by_session == 'price':
                products = products.order_by('sale_price')
            elif order_by_session == 'alphabetic':
                products = products.order_by('title')
            elif order_by_session == 'date':
                products = products.order_by('date')


            
        #Get Quick View
        quick_view = request.GET.get('quick_view')
        del_session = request.GET.get('del_session')
        
        if del_session:
            del request.session['quick_view']
            return redirect('shop')

        if quick_view:
            request.session['quick_view'] = quick_view 
            print(quick_view)

        if request.session.get('quick_view'):
            quick_view = request.session.get('quick_view')
            quick_view_product = Product.objects.get(id=quick_view)
            quick_view_images = Product_Image.objects.filter(product__id=quick_view).first()
            print(request.session.get('quick_view'))
            data={
                'categories':categorys,
                'products':products,
                'quick_view_product':quick_view_product,
                'quick_view_image':quick_view_images,
            }
            return render(request, 'shop.html', data)


        data={
            'categories':categorys,
            'products':products,
            'length':len(products),
        }
        return render(request, 'shop.html', data)
    
    def post(self, request):

        wishlist_id = request.POST.get('wish_id')
        cart_id = request.POST.get('add_cart_id')

        add_id = request.POST.get('add_id')
        minus_id = request.POST.get('minus_id')

        if add_id:
            response_message = Increment_to_Cart(request, add_id)
            return redirect('shop')
        
        if minus_id:
            response_message = decrement_to_Cart(request, minus_id)
            return redirect('shop')

        if wishlist_id:
            response_message = Add_to_wishlist(request, wishlist_id)
            messages.success(request, response_message)
            return redirect('shop')
        
        if cart_id:
            response_message = Add_to_Cart(request, cart_id)
            messages.success(request, response_message)
            return redirect('shop')
        
        return redirect('shop')