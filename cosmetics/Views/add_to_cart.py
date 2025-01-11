from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404
from app.models.banner import Banner
from app.models.category import Category
from app.models.offers import Offers
from app.models.cart import Cart
from app.models.cart_item import Cart_item
from app.models.wishlist import Wishlist
from app.models.wish_item import Wish_item
from app.models.product import Product, Product_Image
from django.http import JsonResponse

def Add_to_wishlist(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            try:
                wishlist_object, created = Wishlist.objects.get_or_create(user=request.user)
                wish_item, created_item = Wish_item.objects.get_or_create(wish=wishlist_object, product=id_exists)            
               
                if created_item:
                    response_message = f"{id_exists.title} has been added in Your Wishlist"
                    print(response_message)
                    return response_message
                else:
                    response_message = "You have already added this product in wishlist!"
                    print(response_message)
                    return response_message

                
            except Exception as e:
               print(e)
        else:
           
            temporary_wish_list = request.session.get('wishlist', {})
            if str(product_id) in temporary_wish_list:
                response_message = "This Product is already in your Wishlist"
                return response_message
            else:
                temporary_wish_list[str(product_id)] = id_exists.slug
                request.session['wishlist'] = temporary_wish_list 
                response_message = f"{id_exists.title} has been added in your Wishlist"
                print(temporary_wish_list)
                return response_message
                     
    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}

    
    return 0



def Add_to_Cart(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            try:
                cart_object, created = Cart.objects.get_or_create(user=request.user)
                cart_item, created_item = Cart_item.objects.get_or_create(cart=cart_object, product=id_exists, quantity=1, total_price=id_exists.sale_price)            

                if created_item:
                    if id_exists.stock > 1:
                        id_exists.stock -= 1
                        id_exists.save() 
                        response_message = f"{id_exists.title} has been added in Your Cart"
                        print(response_message)
                        return response_message
                    else:
                        response_message = f"{id_exists.title} is currently Out of Stock please try later!"
                        print(response_message)
                        return response_message
                else:
                    response_message = "You have already added this product in your Cart!"
                    print(response_message)
                    return response_message

                
            except Exception as e:
               print(e)
        else:
           
            temporary_cart_list = request.session.get('cart', {})
            if str(product_id) in temporary_cart_list:     
                response_message = "This Product is already in your Cart"
                return response_message
            else:
                temporary_cart_list[str(product_id)] = 1
                request.session['cart'] = temporary_cart_list 
                if id_exists.stock > 1:
                        id_exists.stock -= 1
                        id_exists.save() 
                        response_message = f"{id_exists.title} has been added in Your Cart"
                        print(temporary_cart_list)
                        return response_message
                else:
                    response_message = f"{id_exists.title} is currently Out of Stock please try later!"
                    print(response_message)
                    return response_message
                     
    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}

    
    return 0



def Increment_to_Cart(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            try:
                
                cart_item = Cart_item.objects.get(cart__user=request.user, product=id_exists)            
                print(cart_item)
                if cart_item and cart_item.product.stock >= cart_item.quantity:
                    cart_item.quantity = cart_item.quantity+1
                    cart_item.save() 
                    cart_price = id_exists.sale_price * cart_item.quantity
                    cart_item.total_price = cart_price
                    cart_item.save() 
                    id_exists.stock -= 1
                    id_exists.save() 
                else:
                    response_message = f"{id_exists.title} is Out of Stock please try later!"
                    print(response_message)
                    return response_message
                    
                
            except Exception as e:
               print(e)
        else:
            temporary_cart_list = request.session.get('cart')
            quantity = temporary_cart_list.get(product_id) 
            if quantity and (id_exists.stock >= quantity):
                quantity = int(quantity)+1
                temporary_cart_list[str(product_id)] = quantity
                request.session['cart'] = temporary_cart_list
                id_exists.stock -= 1
                id_exists.save() 
                print(temporary_cart_list)
            else:
                response_message = f"{id_exists.title}'s is currently Out of Stock please try later!"
                print(response_message)
                return response_message
                        
    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}

    
    return 0



def decrement_to_Cart(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            try:
                cart_item = Cart_item.objects.get(cart__user=request.user, product=id_exists)            
                print(cart_item)
                if cart_item.quantity > 1:
                    cart_item.quantity = cart_item.quantity-1
                    cart_item.save() 
                    cart_price = id_exists.sale_price * cart_item.quantity
                    cart_item.total_price = cart_price
                    cart_item.save() 
                    id_exists.stock += 1
                    id_exists.save() 
                elif cart_item.quantity == 1:
                    cart_item.delete()
                    id_exists.stock += 1
                    id_exists.save() 
                
                
            except Exception as e:
               print(e)
        else:
            temporary_cart_list = request.session.get('cart')
            quantity = temporary_cart_list.get(product_id) 
            if int(quantity) > 1:
                quantity = int(quantity)-1
                temporary_cart_list[str(product_id)] = quantity
                request.session['cart'] = temporary_cart_list
                id_exists.stock += 1
                id_exists.save() 
            elif int(quantity) == 1:
                del temporary_cart_list[product_id]
                request.session['cart'] = temporary_cart_list
                id_exists.stock += 1
                id_exists.save() 

    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}

    
    return 0


def delete_Cart(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            cart_object = Cart.objects.get(user=request.user)
            cart_item = Cart_item.objects.get(cart=cart_object, product=id_exists)            
               
            if cart_item:
                id_exists.stock += cart_item.quantity
                id_exists.save() 
                cart_item.delete()
                response_message = f"{cart_item.product.title} has been removed from your cart"
            return response_message
        else:
            temporary_cart_list = request.session.get('cart')
            product_item = Product.objects.filter(id=product_id).first()            
            if str(product_id) in temporary_cart_list:
                quantity = temporary_cart_list.get(product_id)
                id_exists.stock += quantity
                id_exists.save()   
                del temporary_cart_list[product_id]
                request.session['cart'] = temporary_cart_list
                response_message = f"{product_item.title} has been removed from your cart"
                return response_message
 
    
    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}           
    

def delete_Wish(request, product_id):
    try:
        id_exists = Product.objects.get(id=product_id)
        if request.user.is_authenticated:   
            wish_object = Wishlist.objects.get(user=request.user)
            wish_item = Wish_item.objects.get(wish=wish_object, product=id_exists)            
               
            if wish_item:
                wish_item.delete()
                response_message = f"{wish_item.product.title} has been removed from your wishlist"
            return response_message
        else:
            temporary_wish_list = request.session.get('wishlist')
            product_item = Product.objects.filter(id=product_id).first()
      
            if str(product_id) in temporary_wish_list:  
                del temporary_wish_list[product_id]
                request.session['wishlist'] = temporary_wish_list
                response_message = f"{product_item.title} has been removed from your wishlist"
                return response_message
 
    
    except Exception as e:
            response_message = f"An error Occured:{e}"
            return {'message':response_message}    
   