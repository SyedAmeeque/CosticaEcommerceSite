from django.shortcuts import render, redirect
from django.views import View
# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class Logout(View):

    def get(self, request):

        logout(request)
        messages.error(request, "You are now logged out!")
        return redirect('home')

    
