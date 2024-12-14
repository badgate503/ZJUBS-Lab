import base64

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
from tqdm import tqdm
import time
from bs4 import BeautifulSoup


selenium_grid_url = 'http://localhost:4444/wd/hub'
option = webdriver.FirefoxOptions()

option.set_preference("dom.webdriver.enabled", False)  # 禁用WebDriver标志
option.set_preference("useAutomationExtension", False)  # 禁用自动化扩展
option.set_preference("general.useragent.override", "Mozilla/5.0 ...")  # 模拟真实用户代理
option.add_argument("--disable-blink-features=AutomationControlled")  # 去除自动化特征

driver = None
driver_not_close = False

class queryInfo:
    queryNum = 0
    queryText = ""
    def __init__(self, queryNum, queryText): #必须要有一个self参数，
        self.queryNum = queryNum
        self.queryText = queryText

class itemInfo:
    link = ""
    fromwhich = "taobao"
    img = ""
    name = ""
    price = 0
    def __init__(self,link, fromwhich,img,name,price): #必须要有一个self参数，
        self.link = link
        self.fromwhich = fromwhich
        self.img = img
        self.name = name
        self.price = price

    def __json__(self):
        return self.__dict__

    def __repr__(self):
        return f"Item(name={self.name}, price={self.price}, imglink={self.img})"



def tb_get_qr():
    encoded_png = ""
    global driver
    global driver_not_close
    try:
        driver = webdriver.Remote(command_executor=selenium_grid_url, options=option)
        # with open('./stealth.min.js') as f:
        #     inject_js = f.read()
        # driver.execute_script(inject_js)
        print("Selenium Starts")

        driver.get("https://www.taobao.com")
        driver.implicitly_wait(5)
        logbtn=WebDriverWait(driver,10,1).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-login')))
        logbtn.click()
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[1])
        code = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'qrcode-img')))
        time.sleep(1)
        png = code.screenshot_as_png
        encoded_png = base64.b64encode(png).decode('utf-8')
        print(encoded_png)
        print("QRCode OK")
        driver_not_close = True
        # current_url = driver.current_url
        # WebDriverWait(driver, 30, 1).until(EC.url_changes(current_url))
        # driver.implicitly_wait(40)
        # q = driver.find_element(By.ID, 'q')
        # driver.save_screenshot("tb0.png")
        # dictCookies = driver.get_cookies()
        # jsonCookies = json.dumps(dictCookies)
        # # 登录完成后,将cookies保存到本地文件
        # with open("../cookies_tao.json", "w") as fp:
        #     fp.write(jsonCookies)
    except Exception as e:
        print("Error occurs!")
        print(e)
        driver.quit()
        driver_not_close=False
    return encoded_png

def tb_get_cookie():
    global driver
    global driver_not_close
    jsonCookies = ""
    if(driver_not_close):
        try:
            current_url = driver.current_url
            WebDriverWait(driver, 30, 1).until(EC.url_changes(current_url))
            driver.implicitly_wait(200)
            q = driver.find_element(By.ID, 'q')
            driver.save_screenshot("tb0.png")
            time.sleep(1)
            dictCookies = driver.get_cookies()
            jsonCookies = json.dumps(dictCookies)
        except Exception as e:
            print("Error!")
        finally:
            driver.quit()
            driver_not_close=False
            return jsonCookies
    return jsonCookies


def close_driver():
    global driver
    global driver_not_close
    if(driver_not_close):
        driver.quit()
        driver_not_close = False

def tb_searchItem(queryInfo, cookie):
    try:
        fetchItemList = []
        driver = webdriver.Remote(command_executor=selenium_grid_url, options=option)
        options = Options()
        options.add_argument("--headless")
        # 初次建立连接, 随后方可修改cookie
        driver.get('http://www.taobao.com')
        # 删除第一次登录是储存到本地的cookie
        driver.delete_all_cookies()
        # 读取登录时储存到本地的cookie
        ListCookies = json.loads(cookie)

        for cookie in ListCookies:
            driver.add_cookie({
                'domain': '.taobao.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })

        # 再次访问页面，便可实现免登陆访问
        driver.get("https://www.taobao.com")
        driver.implicitly_wait(5)
        print("Taobao Logon!")
        q = driver.find_element(By.ID, 'q')

        q.send_keys(queryInfo.queryText)
        searchSubmit = driver.find_element(By.CLASS_NAME, "btn-search")
        searchSubmit.click()
        wait = WebDriverWait(driver, 10)
        for i in range(2,70):   #也可以设置一个较大的数，一下到底
            js = "var q=document.documentElement.scrollTop={}".format(i*100)  #javascript语句
            time.sleep(0.05)
            driver.execute_script(js)

        html = driver.page_source


        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        elements = soup.find_all(class_=lambda class_name: class_name and class_name.startswith('mainPicAndDesc--'))
        for element in elements:
            parent_href = element.parent.parent['href']
            img = element.find('img', class_=lambda class_name: class_name and class_name.startswith('mainPic'))
            img_src = img['src'] if img else "No image"

            # 获取 classname 以 "title" 开头的 div 的文本
            title_div = element.find('div', class_=lambda class_name: class_name and class_name.startswith('title'))
            title_text = title_div.text.strip() if title_div else "No title"

            # 获取 classname 以 "pricewrapper" 开头的 div 下第一个 div 的文本
            price_div = element.find('div', class_=lambda class_name: class_name and class_name.startswith('priceWrapper'))
            first_price = price_div.find('div').text.strip() if price_div and price_div.find('div') else "No price"


            fetchItemList.append(itemInfo(link=parent_href, fromwhich="taobao", img=img_src, name=title_text, price=first_price).__dict__)

        return fetchItemList




        # driver.implicitly_wait(10)
        # itemList = driver.find_elements(By.XPATH, "//*[@id='content_items_wrapper']/div")
        # driver.execute_script("window.scrollBy(0,600)")
        # print("Item list fetched!")
        #
        # for item in tqdm(itemList):
        #     driver.execute_script("window.scrollBy(0,120)")
        #     driver.implicitly_wait(5)
        #     link = item.get_attribute("href")
        #     wait = WebDriverWait(driver, 10, 0.1)
        #     img = item.find_element(By.XPATH, ".//div[1]/div[1]/div[1]/img[1]").get_attribute("src")
        #     name = item.find_element(By.XPATH, ".//div[1]/div[1]/div[2]/div[1]/span").text
        #     priceInt = item.find_element(By.XPATH, ".//div[1]/div[1]/div[4]/div[1]/span[1]").text
        #     priceFloat = item.find_element(By.XPATH, ".//div[1]/div[1]/div[4]/div[1]/span[2]").text
        #     fetchItemList.append(itemInfo(link=link, fromwhich="taobao", img=img,name=name,price=int(priceInt)*100+int(priceFloat[1:2])).__dict__)
        # return fetchItemList

    except Exception as e:
        print("Error occurs!")
        print(e)
    finally:
        driver.quit()
        print("Driver abort!")


def jd_get_qr():
    encoded_png = ""
    global driver
    global driver_not_close
    try:
        driver = webdriver.Remote(command_executor=selenium_grid_url, options=option)
        print("Selenium Starts")

        driver.get("https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2F")
        code = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'passport-main-qrcode-img')))
        time.sleep(1)
        png = code.screenshot_as_png
        encoded_png = base64.b64encode(png).decode('utf-8')
        print(encoded_png)
        print("JD QRCode OK")
        driver_not_close = True
    except Exception as e:
        print("Error occurs!")
        print(e)
        driver.quit()
        driver_not_close=False
    return encoded_png

def jd_get_cookie():
    global driver
    global driver_not_close
    jsonCookies = ""
    if(driver_not_close):
        try:
            current_url = driver.current_url
            WebDriverWait(driver, 30, 1).until(EC.url_changes(current_url))
            driver.implicitly_wait(200)
            q = driver.find_element(By.ID, 'J_searchbg')
            driver.save_screenshot("tb0.png")
            time.sleep(1)
            dictCookies = driver.get_cookies()
            jsonCookies = json.dumps(dictCookies)
        except Exception as e:
            print("Error!")
        finally:
            driver.quit()
            driver_not_close=False
            return jsonCookies
    return jsonCookies


def jd_searchItem(queryInfo, cookie):
    try:
        fetchItemList = []
        driver = webdriver.Remote(command_executor=selenium_grid_url, options=option)
        options = Options()
        options.add_argument("--headless")
        # 初次建立连接, 随后方可修改cookie
        driver.get('https://www.jd.com')
        # 删除第一次登录是储存到本地的cookie
        driver.delete_all_cookies()
        # 读取登录时储存到本地的cookie
        ListCookies = json.loads(cookie)

        for cookie in ListCookies:
            driver.add_cookie({
                'domain': '.jd.com',  # 此处xxx.com前，需要带点
                'name': cookie['name'],
                'value': cookie['value'],
                'path': '/',
                'expires': None
            })

        # 再次访问页面，便可实现免登陆访问
        driver.get("https://www.jd.com")
        driver.implicitly_wait(5)
        print("Jingdong Logon!")
        q = driver.find_element(By.ID, 'key')

        q.send_keys(queryInfo.queryText)
        searchSubmit = driver.find_element(By.CLASS_NAME, "button")
        searchSubmit.click()
        wait = WebDriverWait(driver, 10)
        for i in range(2,70):   #也可以设置一个较大的数，一下到底
            js = "var q=document.documentElement.scrollTop={}".format(i*100)  #javascript语句
            time.sleep(0.05)
            driver.execute_script(js)

        html = driver.page_source


        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html, 'html.parser')

        product_divs = soup.find_all('div', class_='gl-i-wrap')

        print(product_divs)
        for product in product_divs:
            try:
                # 获取图片的src
                img_tag = product.find('div', class_='p-img').find('a').find('img')
                img_src = img_tag['src'] if img_tag else None

                # 获取价格的text
                price_tag = product.find('div', class_='p-price').find('strong').find('i')
                price = price_tag.text.strip() if price_tag else None

                # 获取名字的text
                name_tag = product.find('div', class_='p-name').find('a').find('em')
                name = name_tag.text.strip() if name_tag else None

                # 获取链接的href
                link_tag = product.find('div', class_='p-img').find('a')
                link = link_tag['href'] if link_tag else None

                # 将数据存储到列表中
                fetchItemList.append(itemInfo(link=link, fromwhich="jingdong", img=img_src, name=name, price=price).__dict__)
            except Exception as e:
                print(f"Error processing product: {e}")
        return fetchItemList




        # driver.implicitly_wait(10)
        # itemList = driver.find_elements(By.XPATH, "//*[@id='content_items_wrapper']/div")
        # driver.execute_script("window.scrollBy(0,600)")
        # print("Item list fetched!")
        #
        # for item in tqdm(itemList):
        #     driver.execute_script("window.scrollBy(0,120)")
        #     driver.implicitly_wait(5)
        #     link = item.get_attribute("href")
        #     wait = WebDriverWait(driver, 10, 0.1)
        #     img = item.find_element(By.XPATH, ".//div[1]/div[1]/div[1]/img[1]").get_attribute("src")
        #     name = item.find_element(By.XPATH, ".//div[1]/div[1]/div[2]/div[1]/span").text
        #     priceInt = item.find_element(By.XPATH, ".//div[1]/div[1]/div[4]/div[1]/span[1]").text
        #     priceFloat = item.find_element(By.XPATH, ".//div[1]/div[1]/div[4]/div[1]/span[2]").text
        #     fetchItemList.append(itemInfo(link=link, fromwhich="taobao", img=img,name=name,price=int(priceInt)*100+int(priceFloat[1:2])).__dict__)
        # return fetchItemList

    except Exception as e:
        print("Error occurs!")
        print(e)
    finally:
        driver.quit()
        print("Driver abort!")








