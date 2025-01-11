from django.shortcuts import render, redirect
from django.views import View
from app.models.cart_item import Cart_item
from django.db.models import Sum
from .add_to_cart import Increment_to_Cart, decrement_to_Cart, delete_Cart
from django.contrib import messages

# Create your views here.

class Cart(View):

    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart_item.objects.filter(cart__user = request.user)
            
            if cart_items:
                total_sum_price = Cart_item.objects.filter(cart__user=request.user).aggregate(total_sum=Sum('total_price'))['total_sum']
                free_shipping_remaining_price = 900 - total_sum_price 
            else:
                total_sum_price = 0
                free_shipping_remaining_price = 900
            data={
                'cart_items':cart_items,
                'cart_length':len(cart_items),
                'total_price':total_sum_price,
                'remaining_price':free_shipping_remaining_price,
            } 
            return render(request, 'cart.html',data)
        return render(request, 'cart.html')
    
    def post(self, request):
        add_id = request.POST.get('add_id')
        minus_id = request.POST.get('minus_id')
        delete_id = request.POST.get('delete_id')

        if add_id:
            response_message = Increment_to_Cart(request, add_id)
            messages.success(request, response_message)
            return redirect('cart')
        
        if minus_id:
            response_message = decrement_to_Cart(request, minus_id)
            messages.success(request, response_message)
            return redirect('cart')
        
        if delete_id:
            response_message = delete_Cart(request, delete_id)
            messages.success(request, response_message)
            return redirect('cart')
        
        return redirect('cart')