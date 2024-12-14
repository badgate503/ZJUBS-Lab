from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.middleware.csrf import get_token ,rotate_token
from django.core.mail import send_mail

from . import models
from .Spider.spiengine import queryInfo, itemInfo, tb_get_qr, tb_searchItem, close_driver, tb_get_cookie

import json

from .models import user_profile

from .utils import saveSearchResult, queryItems


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def send_email(request):
    send_mail(
        subject='欢迎注册比比价',
        message='您的验证码为 114514',
        from_email='bibijia1011@163.com',
        recipient_list=[request.user.username],
        fail_silently=False
    )
    return HttpResponse('OK')


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
        user_prof = user_profile(user=user, user_tb_token=None)
        user_prof.save()
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

def tb_get_qrcode(request):
    print("GET QR")
    img = tb_get_qr()
    return JsonResponse({'status': 'success', 'img':img})

def db_fetchItem(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    res = queryItems(query_name)
    print(res)

def tb_fetchItem(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    q = queryInfo(queryNum=0, queryText=query_name)
    cookie = request.user.profile.user_tb_token
    res = tb_searchItem(q,cookie)

    resJson=json.dumps(res)
    saveSearchResult(res, query_name)
    return HttpResponse(resJson)

def shut_driver(request):
    close_driver()
    return JsonResponse({'status': 'success'})

def tb_cookie(request):
    cookie = tb_get_cookie()
    user_prof = request.user.profile  # 假设 request.user 已登录
    user_prof.user_tb_token = cookie
    user_prof.save()
    if cookie != "":
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'failure'})

