import requests
import os
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
hero_list_url = 'https://pvp.qq.com/web201605/js/herolist.json'
hero_list_info = requests.get(hero_list_url, headers=headers)
# print(hero_list_info.json())
for h in hero_list_info.json():
    # print(type(h))
    cname = h.get('cname')
    ename = h.get('ename')
    if not os.path.exists(cname):
        os.makedirs(cname)
    hero_image_url = f"https://pvp.qq.com/web201605/herodetail/{ename}.shtml"
    hero_image_resp = requests.get(hero_image_url, headers=headers)
    hero_image_resp.encoding = 'gbk'
    e = etree.HTML(hero_image_resp.text)
    hero_names = e.xpath('//ul[@class="pic-pf-list pic-pf-list3"]/@data-imgname')[0]
    if '|' in hero_names and '&' in hero_names:
        hero_names = (hero_name[0:hero_name.find('&')] for hero_name in hero_names.split('|'))
        for i, n in enumerate(hero_names):
            image_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-{i + 1}.jpg"
            image_url_resp = requests.get(image_url, headers=headers)
            with open(f'{cname}/{n}.jpg', 'wb') as f:
                # print(type(image_url_resp))
                f.write(image_url_resp.content)
            print(f'{n} download  succeed')
    elif '|' in hero_names:
        hero_names = hero_names.split('|')
        # print(hero_names)
        for i in range(len(hero_names)):
            image_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-{i + 1}.jpg"
            image_url_resp = requests.get(image_url, headers=headers)
            name = hero_names[i]
            # print(name)
            with open(f'{cname}/{name}.jpg', 'wb') as f:
                # print(type(image_url_resp))
                f.write(image_url_resp.content)

            print(f'{name} download  succeed')

    else:
        image_url = f"https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{ename}/{ename}-bigskin-1.jpg"
        image_url_resp = requests.get(image_url, headers=headers)
        name = hero_names[0:hero_names.index('&')]
        with open(f'{cname}/{name}.jpg', 'wb') as f:
            # print(type(image_url_resp))
            f.write(image_url_resp.content)
            # save images into  folder 
        print(f'{name} download  succeed')



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from lxml import etree

options = webdriver.ChromeOptions()
options.add_argument("headless")

driver = webdriver.Chrome(options=options)

url = "https://zoom.us/zh-cn/download#client_4meeting"
driver.get(url)

try:
    element_present = EC.presence_of_element_located((By.XPATH, '//a[@class="download-btn-lk zm-button--primary zm-button--large zm-button is-link"]'))
    WebDriverWait(driver, 10).until(element_present)

    tree = etree.HTML(driver.page_source)
    download_link = tree.xpath('//a[@class="download-btn-lk zm-button--primary zm-button--large zm-button is-link"]/@href')
    
    if download_link:
        print(download_link[0])
    else:
        print("Download link not found")

except TimeoutException:
    print("Timed out waiting for page to load")

except NoSuchElementException as nse:
    print("Element not found:", nse)

except Exception as e:
    print("Error occurred:", e)

finally:
    driver.quit()

