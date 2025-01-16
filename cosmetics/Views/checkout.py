from django.shortcuts import render, redirect
from django.views import View
from app.models.user_detail import customer_details
from app.models.cart_item import Cart_item
from app.models.order_info import Order_info
from app.models.order import Order
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from django.core.mail import EmailMessage


class Checkout(View):

    def get(self, request):
        if request.user.is_authenticated:
            try:
                total_sum_price = Cart_item.objects.filter(cart__user=request.user).aggregate(total_sum=Sum('total_price'))['total_sum']
            except Exception as e:
                total_sum_price  = 0
            
            print(total_sum_price)

            if total_sum_price is None:
                free_shipping_remaining_price = 900
            else:
                if total_sum_price > 900:
                    free_shipping_remaining_price = total_sum_price - 900
                elif total_sum_price < 900: 
                    free_shipping_remaining_price = 900 - total_sum_price 
            
            data={
                'remaining_price':free_shipping_remaining_price,
            } 
            return render(request, 'checkout.html',data)
        return render(request, 'checkout.html')
    
    def post(self, request):
        name= request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        city=request.POST.get('location')
        address=request.POST.get('address')
        ids_list=request.POST.get('ids_list')
        shipping_charges=0
        delivery_charges=50
        total_order_amount = 0
        make_ids_list = ids_list.split(',')
        make_ids_int_list = [] 

        if ids_list:
            for id in make_ids_list:
                make_ids_int_list.append(int(id))
        else:
            messages.error(request, "Please select the products you want to checkout!")
            return redirect('checkout')
        
        print("make_ids_int_list:", make_ids_int_list)
        
        if city == 'Hyderabad':
            shipping_charges = 100
        elif total_order_amount >= 900:
            shipping_charges = 0
        else:
            shipping_charges = 200

        print("shipping_charges:", shipping_charges)

        if request.user.is_authenticated:
            try:
                get_cart_items = Cart_item.objects.filter(cart__user=request.user, product__id__in = make_ids_int_list)
                print(get_cart_items)

                for item in get_cart_items:
                    total_order_amount += item.total_price
                
                print("order amount: ", total_order_amount)
                
                try:
                    order_details = Order_info.objects.create(
                        user=request.user,
                        name=name,
                        phone=phone,
                        email=email,
                        shipping_address=address,
                        delivery_charges=Decimal(delivery_charges),
                        shipping_charges=Decimal(shipping_charges),
                        total_order_amount=Decimal(total_order_amount)
                        )
                    print(order_details)
                except Exception as e:
                    print(e)
                
                for item in get_cart_items:
                    make_order = Order.objects.create(order_details=order_details,product=item.product,quantity=item.quantity,total_price=item.total_price) 
                    print(make_order)                       
                get_cart_items.delete()
          
                subject = 'Your Order has been Placed Successfully'
                html_message = f'''
                <p>Your order id is : <strong>{order_details.order_id}</strong></p>
                <p>Your Email: <strong>{email}</strong></p>
                <p>Your Order Amount with delivery or shipping charges is: <strong>{order_details.total_order_amount}</strong></p>
                <p>Your phone number: <strong>{phone}</strong></p>
                <p>You can track your order by calling on this number and telling your order-id: <strong>03574673672</strong></p>   
                '''
                from_email = 'mediaproductionart05@gmail.com'
                recipient_list = [email]

                email = EmailMessage(subject, html_message, from_email, recipient_list)
                email.content_subtype = 'html'  # Specify HTML content type
                email.send()

                admin_subject = 'An Order has been Placed Successfully by a Customer'
                admin_html_message = f'''
                <p>Order id is : <strong>{order_details.order_id}</strong></p>
                <p>Customer Name is: <strong>{name}</strong></p>
                <p>Customer Email is: <strong>{order_details.email}</strong></p>
                <p>Customer phone number: <strong>{phone}</strong></p>
                <p>Customer shipping address: <strong>{address}</strong></p>
                <p>Order Amount with delivery or shipping charges is: <strong>{order_details.total_order_amount}</strong></p>
                <p>Shipping charges: <strong>{shipping_charges}</strong></p>
                <p>delivery charges: <strong>{delivery_charges}</strong></p>
                <p>Date: <strong>{order_details.date}</strong></p>   
                <p><strong>Check product details in the website by matching this order id.</strong></p>   
                '''
                admin_from_email = 'mediaproductionart05@gmail.com'
                admin_recipient_list = ['mediaproductionart05@gmail.com']

                admin_email = EmailMessage(admin_subject, admin_html_message, admin_from_email, admin_recipient_list)
                admin_email.content_subtype = 'html'  # Specify HTML content type
                admin_email.send()


                messages.success(request, f"Your Order has been Placed Successfully! Your Order-Id is {order_details.order_id}")
                return redirect('checkout')
            except Exception as e:
                messages.error(request, f"An error has been occured Please Try Again")
                return redirect('checkout')
        else:
            messages.error(request, f"You have to Login first, to Checkout")
            return redirect('checkout')
        
        return redirect('checkout')
      