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
from .Spider.spiengine import queryInfo, itemInfo, tb_get_qr, tb_searchItem, close_driver, tb_get_cookie, jd_get_cookie, jd_searchItem, jd_get_qr

import json

from .models import user_profile, collect_record, product_keyword, product_keyword_general

from .utils import saveSearchResult, queryItems, queryKeyword


# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

def send_email(request):
    json_result = json.loads(request.body)


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
        user_exist = User.objects.filter(first_name=nickname)
        if(len(user_exist) != 0): return HttpResponse("duplicate")
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
        user_prof = user_profile(user=user, user_tb_token=None, user_jd_token=None)
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
            'userEmail': current_user.username,
            'userTBLogged': (current_user.profile.user_tb_token != None),
            'userJDLogged': (current_user.profile.user_jd_token != None),
        }
        return HttpResponse(json.dumps(data))

def logout(request):
    auth.logout(request)
    return HttpResponse("OK")

def tb_get_qrcode(request):
    print("GET QR")
    img = tb_get_qr()
    return JsonResponse({'status': 'success', 'img':img})

def jd_get_qrcode(request):
    print("GET QR")
    img = jd_get_qr()
    return JsonResponse({'status': 'success', 'img':img})

def fetchItem(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    existKeyWords = queryKeyword(query_name)
    print(json_result['forceUpdate'])
    if len(existKeyWords) != 0 and (not json_result['forceUpdate']):
        keywordInfo = existKeyWords[0]
        res = queryItems(query_name)
    else:
        q = queryInfo(queryNum=0, queryText=query_name)
        tb_cookie = request.user.profile.user_tb_token
        jd_cookie = request.user.profile.user_jd_token
        if (tb_cookie is None) or (jd_cookie is None):
            return HttpResponse(json.dumps({"state":"notlogin"}))
        res1=[]
        res2=[]
        if(tb_cookie != ""):
            res1 = tb_searchItem(q,tb_cookie)
        if(jd_cookie != ""):
            res2 = jd_searchItem(q,jd_cookie)
        if(res1 != None and res2 != None):
            res = res1+res2
        elif res1 != None:
            res = res1
        elif res2 != None:
            res = res2
        else:
            return HttpResponse("nores")
        keywordInfo = saveSearchResult(res, query_name)


    ret = {
        "state":"ok",
        "keyInfo":keywordInfo,
        "qRes":res
    }
    print(ret)
    return HttpResponse(json.dumps(ret))



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

def jd_cookie(request):
    cookie = jd_get_cookie()
    user_prof = request.user.profile  # 假设 request.user 已登录
    user_prof.user_jd_token = cookie
    user_prof.save()
    if cookie != "":
        return JsonResponse({'status':'success'})
    else:
        return JsonResponse({'status':'failure'})

def favorKey(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    exist_collect = collect_record.objects.filter(product_keyword=query_name, user_profile=request.user)
    if(len(exist_collect)!=0):
        return HttpResponse("exist")
    new_collect = collect_record(user_profile=request.user, product_keyword=query_name, need_notify=False)
    new_collect.save()
    return HttpResponse("OK")

def favorNotify(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']

    new_need = json_result['new_need']
    if new_need and (request.user.profile.user_jd_token == None or request.user.profile.user_tb_token == None): return HttpResponse("notalllogin")
    exist_collect = collect_record.objects.filter(user_profile=request.user, product_keyword=query_name)[0]
    exist_collect.need_notify = new_need
    exist_collect.save()
    return HttpResponse("OK")

def get_keyword_info(request):
    collect_list = list(collect_record.objects.filter(user_profile=request.user).values("product_keyword", "need_notify"))
    infoList=[]
    for keyword in collect_list:
        print(keyword['product_keyword'])
        ll = product_keyword_general.objects.filter(keyword_name=keyword['product_keyword'])[0].lowest_link
        latestInfo = { "keyInfo": queryKeyword(keyword['product_keyword'])[0], "need_notify":keyword['need_notify'], "lowest_link":ll}
        infoList.append(latestInfo)
    print(infoList)
    return HttpResponse(json.dumps(infoList))

def remove_favor(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    favor_record = collect_record.objects.filter(user_profile=request.user, product_keyword=query_name)
    favor_record.delete()
    return HttpResponse("OK")

def getPriceChange(request):
    json_result = json.loads(request.body)
    query_name = json_result['query_name']
    records = list(product_keyword.objects.filter(keyword_name=query_name).order_by('update_time').values("update_time", "TBavgPrice", "JDavgPrice", "minPrice"))
    renamed_result = [
        {'update_time': item['update_time'].strftime('%Y-%m-%d %H:%M:%S'), 'minPrice':item['minPrice'], 'TBavgPrice':item['TBavgPrice'], 'JDavgPrice':item['JDavgPrice']}
        for item in records
    ]
    return HttpResponse(json.dumps(renamed_result))