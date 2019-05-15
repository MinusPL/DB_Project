from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from dbhandler.models import CustomUser

# Create your views here.

def register(request):
    #get form values
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['lats_name']
        user_name = request.POST['user_name']
        email = request.POST['first_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        #check if password match
        if password == password2:
            #check username
            if User.object.filter(user_name=user_name).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                #check email
                if User.object.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.object.create_user(user_name=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You are now registered')
                    return redirect('login')
        else:
            messages.success(request, 'Password no not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    #login user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == POST:
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
