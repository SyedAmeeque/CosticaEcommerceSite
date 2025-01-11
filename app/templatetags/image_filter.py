from django import template
from ..models.product import Product_Image,Product
from django.contrib.auth.models import User
from ..models.cart_item import Cart_item
from ..models.wishlist import Wishlist
from ..models.wish_item import Wish_item
from ..models.order import Order
from ..models.category import Category
from django.contrib.auth.models import User
from django.db.models import Sum

register = template.Library()

@register.filter(name="filter_one_image")
def filter_one_image(product):
    image = Product_Image.objects.filter(product=product).first()
    
    return image.image.url

@register.filter(name="filter_product_image")
def filter_product_images(product):
    images = Product_Image.objects.filter(product=product)
    if images:
        return images[0:2:1]
    
    return 0

@register.filter(name="check_cart_contains")
def Check_Cart(product_id, user):
    cart_item_exists = Cart_item.objects.filter(cart__user=user, product__id=product_id).first()
    if cart_item_exists:
        return True
    
    return False

@register.filter(name="check_cart_session")
def Check_Cart_session(product_id, cart):
    if str(product_id) in cart:
        return True
    
    return False



@register.filter(name="check_wishlist_contains")
def Check_Wishlist(product_id, user):
    wish_item_exists = Wish_item.objects.filter(wish__user=user, product__id=product_id).first()
    if wish_item_exists:
        return True
    
    return False

@register.filter(name="check_wish_session")
def Check_Wish_session(product_id, wishlist):
    if str(product_id) in wishlist:
        return True
    
    return False


@register.filter(name="get_wish_length")
def get_wish_length(wishlist):
    if wishlist is not None:
        return len(wishlist)

    return 0



@register.filter(name="get_wish_length_model")
def get_wish_length_model(user):
    if user:
        items = Wish_item.objects.filter(wish__user=user) 
        return len(items)
    
    return 0


    
@register.filter(name="get_cart_length")
def get_cart_length(cart):
    if cart is not None:
        return len(cart)

    return 0



@register.filter(name="get_cart_length_model")
def get_cart_length_model(user):
    if user:
        items = Cart_item.objects.filter(cart__user=user) 
        return len(items)
    
    return 0


@register.filter(name="get_cart_items")
def get_cart_items(user):
    if user:
        all_items=[]
        items = Cart_item.objects.filter(cart__user=user) 
        for i in items:
            image = Product_Image.objects.filter(product=i.product).first() 
            all_items.append((i, image))
        return all_items
    message = "Your cart is empty"
    return message

@register.filter(name="get_cart_items_session")
def get_cart_items_session(cart):
    if cart:
        cart_items = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            total_prices = product.sale_price * quantity
            cart_items.append((product, quantity, total_prices))
        return cart_items
    return []   

@register.filter(name="get_wish_items_session")
def get_wish_items_session(wishlist):
    if wishlist:
        wish_items = []
        for product_id, quantity in wishlist.items():
            product = Product.objects.get(pk=product_id)
            total_prices = product.sale_price
            wish_items.append((product, quantity, total_prices))
        return wish_items
    return [] 

@register.filter(name="get_cart_items_session_with_image")
def get_cart_items_session_with_image(cart):
    if cart:
        cart_items = []
        for product_id, quantity in cart.items():
            product = Product.objects.get(pk=product_id)
            product_image = Product_Image.objects.filter(product=product).first()
            cart_items.append((product, quantity, product_image))
        return cart_items
    return []   


    
@register.filter(name="get_quantity_user")
def check_cart_quantity_user(product, user):
    
    check_cart = Cart_item.objects.filter(cart__user=user, product=product).first()
    if check_cart:
        print(check_cart.quantity)
        return check_cart.quantity
    
    return 1




@register.filter(name="get_quantity_session")
def check_cart_quantity_session(product_id, cart):
    item = cart.get(str(product_id))
    if item:
        print(item)
        return item
    
    return 1
        

@register.filter(name="get_total_price_user")
def get_total_price_user(user):
    
    total_sum_price = Cart_item.objects.filter(cart__user=user).aggregate(total_sum=Sum('total_price'))['total_sum']
    print(total_sum_price)
    if total_sum_price:
        return total_sum_price

    return 0

@register.filter(name="get_total_price_session")
def get_total_price_session(cart):
    if cart:
        keys = list(cart.keys())
        products = Product.objects.filter(id__in=keys)
        print(products)
        price_list = []
        for p in products:
            quantity = cart.get(str(p.id))
            print(quantity)
            total_price = p.sale_price * quantity
            price_list.append(total_price)
        
        if price_list:
            return sum(price_list)

    return 0

@register.filter(name="get_total_price_session_wishlist")
def get_total_price_session_wishlist(wishlist):
    if wishlist:
        keys = list(wishlist.keys())
        products = Product.objects.filter(id__in=keys)
        print(products)
        price_list = []
        for p in products:
            price_list.append(p.sale_price)
        
        if price_list:
            return sum(price_list)

    return 0

@register.filter(name="get_name_category")
def get_name_category(id):
    
    cat = Category.objects.get(id=id)
    
    return cat.name 



@register.filter(name="get_remaining_price_cart")
def get_remaining_price_cart(cart):    
    total_sum = get_total_price_session(cart)
    print(total_sum)
    total_sum = 900 - total_sum

    return total_sum

   

@register.filter(name="multiply_price_to_get_total")
def multiply_price_to_get_total(quantity, price):    
    if quantity and price:
        return quantity * price
    
    return 0



@register.filter(name="get_orders_length")
def get_orders_length(user):    
    if user:
        orders = Order.objects.filter(order_details__user = user)
        return len(orders)
    
    return 0
