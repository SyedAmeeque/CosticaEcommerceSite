from django.shortcuts import render, redirect
from django.views import View
from app.models.product import Product, Product_Image
from app.models.reviews import Reviews 
from app.models.cart_item import Cart_item 
from .add_to_cart import Add_to_Cart, Add_to_wishlist, Increment_to_Cart, decrement_to_Cart
from django.contrib import messages

# Create your views here.

class Product_View(View):

    def get(self, request, slug):

        product = Product.objects.get(slug__exact=slug)
        get_reviews = Reviews.objects.filter(product=product)
        images = Product_Image.objects.filter(product=product)
        product_category = product.category.all()
        related_products = Product.objects.filter(category__in=product_category).exclude(id=product.id)
        tags = product.tag.all()
        #Get Quick View
        quick_view = request.GET.get('quick_view')
        del_session = request.GET.get('del_session')
        
        if del_session:
            del request.session['quick_view']
            return redirect('product', slug)

        if quick_view:
            request.session['quick_view'] = quick_view 
            print(quick_view)

        if request.session.get('quick_view'):
            quick_view = request.session.get('quick_view')
            quick_view_product = Product.objects.get(id=quick_view)
            quick_view_images = Product_Image.objects.filter(product__id=quick_view).first()
            print(request.session.get('quick_view'))
            data={
                'product':product,
                'images':images,
                'rel_products':related_products,
                'categories':product_category,
                'tags':tags,
                'quick_view_product':quick_view_product,
                'quick_view_image':quick_view_images,
            }
            return render(request, 'product.html', data)
        if get_reviews is not None:
            data={
                'product':product,
                'images':images,
                'rel_products':related_products,
                'categories':product_category,
                'reviews':get_reviews,
                'tags':tags,
            }
        else:
            error_message = 'No Reviews for this product' 
            data={
            'product':product,
            'images':images,
            'rel_products':related_products,
            'categories':product_category,
            'error':error_message,
            'tags':tags,
            }

        return render(request, 'product.html', data)
    
    def post(self, request, slug):

        wishlist_id = request.POST.get('wish_id')
        cart_id = request.POST.get('add_cart_id')

        add_id = request.POST.get('add_id')
        minus_id = request.POST.get('minus_id')
        buy_now_id = request.POST.get('buy_now_id')

        message= request.POST.get('message')
        product_id= request.POST.get('product_id')
        review_star = request.POST.get('review_star')

        if buy_now_id:
            if request.user.is_authenticated:
                try:
                    check_cart = Cart_item.objects.get(cart__user=request.user, product__id=buy_now_id)
                    return redirect('checkout')
                except Cart_item.DoesNotExist:
                    response_message = Add_to_Cart(request, buy_now_id)
                    messages.success(request, response_message)
                    return redirect('checkout')
            else:
                # If the user is not authenticated, handle the session cart
                cart = request.session.get('cart')
                if cart:
                    if cart.get(str(buy_now_id)):  # Changed from cart[buy_now_id] to cart.get(buy_now_id) to avoid KeyError
                        return redirect('checkout')
                else:
                    response_message = Add_to_Cart(request, buy_now_id)
                    messages.success(request, response_message)
                    return redirect('checkout')

        if add_id:
            response_message = Increment_to_Cart(request, add_id)
            return redirect('product', slug)
        
        if minus_id:
            response_message = decrement_to_Cart(request, minus_id)
            return redirect('product', slug)

        if wishlist_id:
            response_message = Add_to_wishlist(request, wishlist_id)
            messages.success(request, response_message)
            return redirect('product', slug)
        
        if cart_id:
            response_message = Add_to_Cart(request, cart_id)
            messages.success(request, response_message)
            return redirect('product', slug)
        
        
            

    

      
        if message and review_star:
            product = Product.objects.get(id=product_id)
            get_reviews = Reviews.objects.filter(user=request.user, product=product)
            if get_reviews:
                response_message = "Your have already given the review for this product!"
                messages.success(request, response_message)
                return redirect('product', slug)
            else:
                review = Reviews.objects.create(user=request.user, message=message,product=product, review=review_star)
                response_message = "Your review has been posted successfully!"
                messages.success(request, response_message)
                return redirect('product', slug)
        else:
            response_message = "Your review can't be saved due to some issue please try again!"
            messages.error(request, response_message)
            return redirect('product', slug)

        return redirect('product', slug)

       

