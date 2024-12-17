from datetime import datetime

from django.db.models import Max

from .Spider.spiengine import queryInfo, tb_searchItem, jd_searchItem
from .utils import saveSearchResult
from .models import *

def print_task():
    print('每日刷新启动！{}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    collect_records = collect_record.objects.filter(need_notify=True).values('product_keyword').distinct()
    print(collect_records)



    for coll in collect_records:
        q = queryInfo(queryNum=0, queryText=coll['product_keyword'])
        the_user = collect_record.objects.filter(need_notify=True, product_keyword=coll['product_keyword'])[0].user_profile.profile
        user_tb_cookie = the_user.user_tb_token
        user_jd_cookie = the_user.user_jd_token
        if(user_tb_cookie != ""):
            res1 = tb_searchItem(q,user_tb_cookie)
        if(user_jd_cookie != ""):
            res2 = jd_searchItem(q,user_jd_cookie)
        if(res1 != None and res2 != None):
            res = res1+res2
        elif res1 != None:
            res = res1
        elif res2 != None:
            res = res2
        else:
            continue
        saveSearchResult(res, coll['product_keyword'])