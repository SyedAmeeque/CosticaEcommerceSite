from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.core.mail import EmailMessage
from django.contrib import messages


class Contact(View):

    def get(self, request):

        return render(request, 'contact.html')
    
    
    def post(self, request):
        name= request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        message=request.POST.get('message')
        try:
            subject = 'An Email from Online cosmetic Site!'
            html_message = f'''
            <p>My name is: <strong>{name}</strong></p>
            <p>My email is: <strong>{email}</strong></p>
            <p>My phone number: <strong>{phone}</strong></p>
            <p>Message: <strong>{message}</strong></p>
            '''
            from_email = email
            recipient_list = ['mediaproductionart05@gmail.com']

            admin_email = EmailMessage(subject, html_message, from_email, recipient_list)
            admin_email.content_subtype = 'html'  # Specify HTML content type
            admin_email.send()


            messages.success(request, f"Your Email has been sent Successfully! We respond to you soon!")
            return redirect('contact')
        except Exception as e:
            messages.error(request, f"Your Email couldn't been sent, Please try again later!")
            return redirect('contact')