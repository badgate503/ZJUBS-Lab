from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.db import IntegrityError

import json
# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def login(request):
    print(request.body)
    json_result = json.loads(request.body)
    print(json_result)
    username = json_result['username']
    password = json_result['pwd']
    user_obj = auth.authenticate(username=username, password=password)
    print(user_obj)

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
            'userName': user_obj.first_name,
            'message': "Register Successfully"
        }
        return HttpResponse(json.dumps(data))