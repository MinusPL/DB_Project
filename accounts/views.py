from django.shortcuts import render, redirect
from django.contrib import messages, auth
from dbhandler.models import CustomUser

# Create your views here.

def register(request):
    #get form values
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']
        #check if password match
        if password == password2:
            #check username
            if CustomUser.objects.filter(username=user_name).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                #check email
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    customUser = CustomUser.objects.create_user(username=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
                    customUser.save()
                    messages.success(request, 'You are now registered')
                    return redirect('login')
        else:
            messages.success(request, 'Password no not match')
            return redirect('register')
    else:
        return render(request, 'register.html')

def login(request):
    #login user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        customUser = auth.authenticate(username=username, password=password)
        if customUser is not None:
            auth.login(request,customUser)
            messages.success(request, 'You are now logged in')
            return redirect('index')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')