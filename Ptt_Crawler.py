#!/usr/bin/env python
# coding: utf-8

# <H1>PTT標題</H1>

# In[ ]:


board = input("輸入英文版名:")
pages = input("查詢頁數")


# In[ ]:


import requests
from bs4 import BeautifulSoup

def get_agree(pages,r,soup):
    button = soup.select('input')
    agree = button[0]["value"]
    agree_url = 'https://www.ptt.cc' + agree
    url = agree_url
    print(url)


    
pages = int(pages)
url = f"https://www.ptt.cc/bbs/{board}/index.html"
requests.get(url)

with open(f"ptt{board}.csv",'w',encoding='utf-8-sig') as file: 
    for page in range(pages):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        div = soup.find_all('div',class_="title")
        for t in div:   
            file.write(t.text)
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        print(f'搜尋第{page+1}頁',end=' ')


# <h1>印出所有標題</h1>
# 輸出至 ptt{board}.txt

# In[ ]:


import pandas as pd
df = pd.read_csv(f"ptt{board}.csv",header=None,delimiter='\\t',encoding='utf-8-sig')
pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
df.to_csv(f"ptt{board}.csv", encoding="utf_8_sig",header=False, index=False)


# <h1>關鍵字</h1>
# 輸出至 ptt{board}_{key}.txt

# #### 複合關鍵字，空格隔開

# In[ ]:


import pandas as pd
import numpy as np

keys = list(input("請輸入關鍵字以空白間隔:").split(" "))
for key in keys:
    mask = df[0].str.contains(key)
    df[mask].to_csv(f'ptt{board}_{key}.csv',encoding='utf-8-sig',header=['標題'])
    with open(f"ptt{board}_{key}.csv",'a',encoding='utf-8-sig') as file:
        file.write("共%d筆"%len(df[mask]))


pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

dataset = pd.DataFrame()
for key in keys:
    data = pd.read_csv(f'ptt{board}_{key}.csv',index_col=None)
    dataset = pd.concat([dataset,data])
dataset= dataset.drop_duplicates(['標題'])
dataset.to_csv(f"ptt{board}_{keys}.csv",encoding='utf-8-sig',index=False)
with open(f"ptt{board}_{keys}.csv",'a',encoding='utf-8-sig') as file:
    file.write("共%d筆"%len(dataset))


# #### 多層單關鍵字

# In[ ]:


import pandas as pd
import numpy as np

def MultiFilter(result):
    times = input('輸入還需要篩選幾次 : ')
    times = eval(times)
    if times > 0 :
        for i in range(times):
            key = input(f'輸入第{i+1}篩選字 : ')
            mask = result[0].str.contains(key)
            result = result[mask]
            result.to_csv(f"ptt{board}_{key}.csv",header=['標題'],encoding='utf-8-sig')
            with open(f"ptt{board}_{key}.csv",'a',encoding='utf-8-sig') as file:
                file.write("\n共%d筆"%len(result))
            print(result)
            print("共%d筆"%len(result))
        
key = input("請輸入關鍵字:")
mask = df[0].str.contains(key)
result = df[mask]
pd.set_option('display.max_rows', None)
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
result.to_csv(f"ptt{board}_{key}.csv",encoding='utf-8-sig',header=['標題'])
with open(f"ptt{board}_{key}.csv",'a',encoding='utf-8-sig') as file:
    file.write("\n共%d筆"%len(result))
print(result)
print("共%d筆"%len(result))
MultiFilter(result)


# <h1>看指定文章</h1>

# ### 可輸入關鍵字但只顯示同關鍵字最先的一篇
# 
# 輸出至 ptt{board}_{target}.txt

# In[ ]:


import requests
from bs4 import BeautifulSoup

target = input("請輸入標題:")
url = f"https://www.ptt.cc/bbs/{board}/index.html"

def GetContent():
    ar = soup.select('div.title > a')
    ar_href = ar[number]['href']
    ar_url = 'https://www.ptt.cc' + ar_href
    aurl = requests.get(ar_url)
    asoup = BeautifulSoup(aurl.text,"html.parser")
    CONTENT = asoup.find(id='main-container').text
    return file.write(ar_url+CONTENT)
    
task = 'continue'
with open(f"ptt{board}_{target}.txt",'w',encoding='utf-8') as file: 
    for page in range(900,pages):
        if task == 'continue':
            r = requests.get(url)
            soup = BeautifulSoup(r.text,"html.parser")
            div = soup.find_all('div',class_="title")
            number = -1
            for t in div:
                number += 1
                if target in t.text:
                    print('Find')
                    GetContent()
                    task = 'complete'
            if task == 'continue':
                btn = soup.select('div.btn-group > a')
                up_page_href = btn[3]['href']
                next_page_url = 'https://www.ptt.cc' + up_page_href
                url = next_page_url
                print(f'搜尋第{page+1}頁',end='')
        else:
            print('task ',task)
            break


# ### 可輸入關鍵字找全部頁面

# In[ ]:


import requests
from bs4 import BeautifulSoup

target = input("請輸入標題:")
url = f"https://www.ptt.cc/bbs/{board}/index.html"

def GetContent():
    ar = soup.select('div.title > a')
    ar_href = ar[number]['href']
    ar_url = 'https://www.ptt.cc' + ar_href
    aurl = requests.get(ar_url)
    asoup = BeautifulSoup(aurl.text,"html.parser")
    CONTENT = asoup.find(id='main-container').text
    file.write(ar_url+CONTENT+"\n")
    return ar_url,CONTENT

with open(f"ptt{board}_{target}.txt",'w',encoding='utf-8') as file: 
    for page in range(pages):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        div = soup.find_all('div',class_="title")
        number = -1
        for t in div:
            number += 1
            if target in t.text:
                print('Find')
                GetContent()
        btn = soup.select('div.btn-group > a')
        up_page_href = btn[3]['href']
        next_page_url = 'https://www.ptt.cc' + up_page_href
        url = next_page_url
        print(f'搜尋第{page+1}頁',end='')
        


# ----------------------------------------------

# ### selenium click in (慢)

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import bs4
# import time
# import pandas as pd
# target = input()
# url = f"https://www.ptt.cc/bbs/{board}/index.html"
# browser = webdriver.Edge("C:\python3.7\edgedriver_win64\msedgedriver.exe")
# browser.get(url)
# for i in range(pages): 
#     try:
#         html = browser.page_source
#         soup = bs4.BeautifulSoup(html,"html.parser")
#         div = soup.find_all('div',class_="title")
#         for t in div:
#             if target in t.text:
#                 browser.find_element_by_link_text(target).click()
#                 print('Find!')
#                 time.sleep(100)
#             else:
#                 print("no",end = ',')
#         try :
#             print(i)
#             buttom = browser.find_element_by_xpath("/html/body/div[2]/div[1]/div[1]/div[2]/a[2]")
#             buttom.click()
#         except:
#             break
#     except :
#         break
# browser.close()
