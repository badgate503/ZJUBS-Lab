from .models import product_item,product_keyword
from django.forms.models import model_to_dict

def saveSearchResult(result, resultKeyWord):
    print(result)
    if len(result)==0 :
        return
    TBtotPrice=0
    JDtotPrice=0
    TBcount = 0
    JDcount = 0
    minPrice=-1
    maxPrice=-1
    objs = product_item.objects.filter(product_keyword=resultKeyWord)
    objs.delete()
    for element in result:
        price = int(float(element['price'])*100)
        fromWhich = element['fromwhich']
        if(fromWhich == "taobao"):
            TBtotPrice += price
            TBcount+=1
        else:
            JDtotPrice += price
            JDcount+=1
        if minPrice == -1:
            minPrice = price
        else:
            minPrice = min(minPrice, price)
        maxPrice = max(maxPrice, price)
        ele = product_item(product_name=str(element['name']), product_keyword=resultKeyWord, price=price, link=str(element['link']), img=str(element['img']), fromwhich=fromWhich)
        ele.save()
    if(JDcount == 0):
        JDavgPrice = 0
    else:
        JDavgPrice = JDtotPrice/JDcount
    if(TBcount==0):
        TBavgPrice = 0
    else:
        TBavgPrice = TBtotPrice/TBcount
    ele_key = product_keyword(keyword_name=resultKeyWord, minPrice=minPrice, maxPrice=maxPrice, TBavgPrice=TBavgPrice, JDavgPrice= JDavgPrice, TBcount=TBcount, JDcount=JDcount)
    ele_key.save()
    return model_to_dict(ele_key)

def queryItems(itemKeyWord):
    products = list(product_item.objects.filter(product_keyword=itemKeyWord).values('link','fromwhich','img','product_name','price'))
    renamed_result = [
        {'link': item['link'], 'name': item['product_name'], 'price': str(float(item['price'])/100), 'fromwhich': item['fromwhich'], 'img': item['img']}
        for item in products
    ]
    return renamed_result

def queryKeyword(itemKeyWord):
    itemKeywordList = list(product_keyword.objects.filter(keyword_name=itemKeyWord).order_by('update_time').values('keyword_name', 'update_time', 'minPrice', 'maxPrice', 'TBavgPrice','JDavgPrice', 'TBcount', 'JDcount'))
    renamed_result = [
        {'keyword_name': item['keyword_name'], 'update_time': item['update_time'].strftime('%Y-%m-%d %H:%I:%S'), 'minPrice':item['minPrice'], 'maxPrice':item['maxPrice'], 'TBavgPrice':item['TBavgPrice'], 'JDavgPrice':item['JDavgPrice'], 'TBcount':item['TBcount'], 'JDcount':item['JDcount']}
        for item in itemKeywordList
    ]
    return renamed_result