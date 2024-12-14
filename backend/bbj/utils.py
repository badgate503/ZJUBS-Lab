from .models import product_item,product_keyword

def saveSearchResult(result, resultKeyWord):
    print(result)
    if len(result)==0 :
        return
    avgPrice=0
    minPrice=0
    maxPrice=-1
    for element in result:
        price = int(float(element['price'])*100)
        avgPrice += price
        if minPrice == -1:
            minPrice = price
        else:
            minPrice = min(minPrice, price)
        maxPrice = max(maxPrice, price)
        ele = product_item(product_name=str(element['name']), product_keyword=resultKeyWord, price=price, link=str(element['link']), img=str(element['img']), fromwhich=element['fromwhich'])
        ele.save()
    ele_key = product_keyword(keyword_name=resultKeyWord, minPrice=minPrice, maxPrice=maxPrice, avgPrice=avgPrice/len(result))
    ele_key.save()
    return ele_key

def queryItems(itemKeyWord):
    products = product_item.objects.filter(product_keyword=itemKeyWord)
    return products