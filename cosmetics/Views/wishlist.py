from django.shortcuts import render, redirect
from django.views import View
from app.models.wish_item import Wish_item
from django.db.models import Sum
from .add_to_cart import delete_Wish, Add_to_Cart
from django.contrib import messages
# Create your views here.

class Wishlist(View):

    def get(self, request):

        if request.user.is_authenticated:
            wish_items = Wish_item.objects.filter(wish__user = request.user)
            total_sum = []

            for a in wish_items:
                total_sum.append(a.product.sale_price)

           
           
            data={
                'wish_items':wish_items,
                'wish_length':len(wish_items),
                'total_price':sum(total_sum),
            } 
            return render(request, 'wishlist.html',data)
        return render(request, 'wishlist.html')
    
    def post(self, request):
     
        delete_id = request.POST.get('delete_id')
        add_id = request.POST.get('add_cart_id')

        if add_id:
            response_message = Add_to_Cart(request, add_id)
            messages.success(request, response_message)
            return redirect('wishlist')
        
        if delete_id:
            response_message = delete_Wish(request, delete_id)
            messages.success(request, response_message)
            return redirect('wishlist')
    
        return redirect('wishlist')