from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.middleware.csrf import get_token ,rotate_token

import json
# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


def login(request):
    if request.method =='GET':
        return HttpResponse(get_token(request))
    json_result = json.loads(request.body)
    username = json_result['username']
    password = json_result['password']
    user_obj = auth.authenticate(request, username=username, password=password)
    print(request.user)
    if(user_obj == None):
        data={
            'isLoginOK': False,
            'userName': None,
            'message': "Login Failed"
        }
        return HttpResponse(json.dumps(data))
    else:
        data={
            'isLoginOK': True,
            'userName': user_obj.first_name,
            'message': "Login Successfully"
        }
        auth.login(request, user_obj)
        print("User "+ user_obj.first_name +" Logged in.")
        return HttpResponse(json.dumps(data))

def register(request):
    json_result = json.loads(request.body)
    print(json_result)
    username = json_result['username']
    password = json_result['pwd']
    nickname = json_result['nickname']
    try:
        user = User.objects.create_user(username=username,password=password,first_name=nickname)
    except IntegrityError:
        data={
            'isRegisterOK': False,
            'userName': None,
            'message': "Register Failed"
        }
        return HttpResponse(json.dumps(data))
    else:
        data={
            'isRegisterOK': True,
            'userName': user.first_name,
            'message': "Register Successfully"
        }
        user.save()
        auth.login(request, user)
        print("User "+ user.first_name +" registered.")
        return HttpResponse(json.dumps(data))


def checkLoginState(request):
    current_user = request.user
    if current_user.is_anonymous:
        data={
            'isLogged': False,
            'userName': 'Anonymous',
        }
        return HttpResponse(json.dumps(data))
    else:
        data={
            'isLogged': True,
            'userName': current_user.first_name,
            'userEmail': current_user.username
        }
        return HttpResponse(json.dumps(data))

def logout(request):
    auth.logout(request)
    return HttpResponse("OK")

