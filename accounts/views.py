from django.shortcuts import render, redirect
from django.contrib import messages, auth
from dbhandler.models import CustomUser
from django.contrib.auth.models import Group
from django.http import HttpResponse
import base64

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
                messages.error(request, 'Nazwa użytkownika zajęta')
                return redirect('register')
            else:
                #check email
                if CustomUser.objects.filter(email=email).exists():
                    messages.error(request, 'Email jest już w użyciu')
                    return redirect('register')
                else:
                    customUser = CustomUser.objects.create_user(username=user_name, password=password, email=email, first_name=first_name, last_name=last_name)
                    customUser.save()
                    my_group = Group.objects.get(name='Użytkownik') 
                    my_group.user_set.add(customUser)
                    messages.success(request, 'Rejestracja zakończona pomyślnie')
                    return redirect('login')
        else:
            messages.error(request, 'Hasła nie są identyczne')
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
            messages.success(request, 'Zalogowano poprawnie')
            return redirect('index')
        else:
            messages.error(request, 'Nieprawidłowa nazwa użytkownika lub hasło')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Wylogowano poprawnie')
        return redirect("login")

def changepassword(request):
    if request.method == 'POST':
        oldpassword=request.POST['oldpassword']
        customUser = auth.authenticate(username=request.user.username, password=oldpassword)
        if customUser is not None:
            newPassword=request.POST['newpassword']
            newPassword2=request.POST['newpassword2']
            if newPassword==newPassword2:
                customUser.set_password(newPassword)
                customUser.save()
                auth.login(request,customUser)
                messages.success(request, 'Haslo zmienione')
                return redirect('userdetailview')
            else:
                messages.error(request, 'Nie udalo sie zmienic hasla')
                return redirect('userdetailview')
        else:
            messages.error(request, 'Nieprawidłowe stare hasło')
            auth.logout(request)
            return redirect('login')
    else:
        return render(request,'changePassword.html')

def UserDataChangeView(request):
    if not request.user.is_authenticated:
        return render(request, 'login_error.html')
    if request.method == 'POST':
        password=request.POST['password']
        customUser = auth.authenticate(username=request.user.username, password=password)
        if customUser is not None:
            firstname=request.POST['first_name']
            lastname = request.POST['last_name']
            email=request.POST['email']
            customUser.first_name=firstname
            customUser.last_name=lastname
            customUser.email=email
            customUser.save()
            messages.success(request, 'Dane zmienione')
            return redirect('userdetailview')
        else:
            messages.error(request, 'Nie udalo sie zmienic danych')
            return redirect('userdetailview')
    else:
        return render(request, 'changeUserData.html')

def loginCas(request):
    textUrl = request.build_absolute_uri() 	#get URL
    urlArray = textUrl.split('response=')	#split after 'response='
    result = base64.b64decode(urlArray[1].encode("utf-8")) 	#decode URL
    #return HttpResponse(result)
    params=result.split()
    username=params[5]
    req=params[8]
    #return HttpResponse(req)
    #customUser = CustomUser.objects.filter(username=params[5]).exists()
    #return HttpResponse(customUser)
    if CustomUser.objects.filter(username=username).exists():
        customUser = CustomUser.objects.get(username=username)
        auth.login(request, customUser)
        messages.success(request, 'Zalogowano poprawnie')
        return redirect('index')
    else:
        customUser = CustomUser.objects.create_user(username=username)
        customUser.save()
        if req.filter('student').exists():
            my_group = Group.objects.get(name='Użytkownik') 
            my_group.user_set.add(customUser)
        auth.login(request,customUser)
        messages.success(request, 'Zalogowano poprawnie')
        return redirect('index')