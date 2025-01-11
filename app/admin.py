from django.contrib import admin
from .models.order_info import Order_info
from .models.banner import Banner 
from .models.brand import Brand 
from .models.cart_item import Cart_item 
from .models.cart import Cart 
from .models.category import Category 
from .models.offers import Offers 
from .models.order import Order 
from .models.product import Product, Product_Image
from .models.reviews import Reviews 
from .models.sale import Sale 
from .models.tags import Tag 
from .models.type import Type 
from .models.wish_item import Wish_item 
from .models.wishlist import Wishlist 
from .models.user_detail import customer_details 
# Register your models here.

class order_info_Admin(admin.ModelAdmin):
    list_display=('order_id','delivery_charges','date')

admin.site.register(Order_info, order_info_Admin)


class Banner_Admin(admin.ModelAdmin):
    list_display=('title','subtitle')


admin.site.register(Banner, Banner_Admin)


class Brand_Admin(admin.ModelAdmin):
    list_display=('brand',)

admin.site.register(Brand, Brand_Admin)


class Cart_item_Admin(admin.ModelAdmin):
    list_display=('cart','quantity','total_price')

admin.site.register(Cart_item, Cart_item_Admin)


class cart_Admin(admin.ModelAdmin):
    list_display=('id','user','date')

admin.site.register(Cart, cart_Admin)


class category_Admin(admin.ModelAdmin):
    list_display=('name', )

admin.site.register(Category, category_Admin)


class offer_Admin(admin.ModelAdmin):
    list_display=('offer_text','offer_discount')

admin.site.register(Offers, offer_Admin)



class order_Admin(admin.ModelAdmin):
    list_display=('id','product','quantity','total_price')

admin.site.register(Order, order_Admin)



class product_Image_Admin(admin.ModelAdmin):
    list_display=('id','image','alternate_text','product')

admin.site.register(Product_Image, product_Image_Admin)

class product_Admin(admin.ModelAdmin):
    list_display=('title','stock','compared_price','sale_price')

admin.site.register(Product, product_Admin)


class reviews_Admin(admin.ModelAdmin):
    list_display=('user','message','review')

admin.site.register(Reviews, reviews_Admin)


class tag_Admin(admin.ModelAdmin):
    list_display=('Tag',)

admin.site.register(Tag, tag_Admin)



class type_Admin(admin.ModelAdmin):
    list_display=('name',)

admin.site.register(Type, type_Admin)



class sale_Admin(admin.ModelAdmin):
    list_display=('sale_off',)

admin.site.register(Sale, sale_Admin)



class wishitem_Admin(admin.ModelAdmin):
    list_display=('id','wish','product')

admin.site.register(Wish_item, wishitem_Admin)



class wishlist_Admin(admin.ModelAdmin):
    list_display=('user','date')

admin.site.register(Wishlist, wishlist_Admin)



class user_detail_Admin(admin.ModelAdmin):
    list_display=('phone','address')

admin.site.register(customer_details, user_detail_Admin)