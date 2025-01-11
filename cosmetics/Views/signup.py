from django.shortcuts import render, redirect
from django.views import View
from app.models.user_detail import customer_details
from django.contrib.auth.models import User
from django.contrib import messages
class Signup(View):

    def get(self, request):
        
        return render(request, 'signup.html')
    
    def post(self, request):
        name= request.POST.get('name')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
   
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        try:
            user = User.objects.create_user(username=name, email=email, password=password)
            user.save()
            user_detail = customer_details.objects.create(user=user,phone=phone,address=address)
            messages.success(request, "Your account has been created successfully!")
            return redirect('login')  # Redirect to the login page after signup
        
        except Exception as e:
            messages.error(request, f"An error occured:{e}")
            return redirect('signup')
        
        return redirect('signup')
        
        
        