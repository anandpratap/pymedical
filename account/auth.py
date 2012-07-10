from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.files import File
from django import http
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

def logoutprocess(request):
    print "here"
    logout(request)
    return HttpResponseRedirect('/login')

def loginview(request):
    return render_to_response('login.html')

def loginprocess(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print user, username, password
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/dash')
        else:
            return HttpResponseRedirect('/login')
    else:
        return HttpResponseRedirect('/login')
