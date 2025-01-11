from django.shortcuts import render, redirect
from django.views import View
from app.models.wish_item import Wish_item
from app.models.order import Order
from django.db.models import Sum
from .add_to_cart import delete_Wish, Add_to_Cart
from django.contrib import messages
# Create your views here.

class Orders(View):

    def get(self, request):

        if request.user.is_authenticated:
        
            orders = Order.objects.filter(order_details__user = request.user)

            if orders:
                data={
                    'orders':orders,
                }
            else:
                data={
                    'error':error_message,
                } 
            return render(request, 'order.html',data)
        
        error_message = "Please Login to see your Orders"
        return render(request, 'order.html', {'error':error_message})
    
    def post(self, request):
     
     
        return redirect('orders')