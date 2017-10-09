from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth

def index(request):

    if request.POST.get("login") and login(request):
        return HttpResponseRedirect('/erpadmin/')
    elif request.POST.get("register"):
        return HttpResponseRedirect('/erpadmin/register')
    
    return render(request, 'index.html', locals())

def login(request):

    if request.user.is_authenticated(): 
        return HttpResponseRedirect('/')

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        auth.login(request, user)
        return True
    else:
        if username != "" or password !="":
          return False

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')