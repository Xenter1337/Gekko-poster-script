import httpx
from bs4 import BeautifulSoup
from twocaptcha import TwoCaptcha
import time
import os


solver = TwoCaptcha('') #api ключ rucaptcha
 


def load_file():
    
    
    client = httpx.Client()
    res = client.get('https://gekkk.co/')
    xsrf = res.cookies.get("XSRF-TOKEN")
    brain = res.cookies.get("brainshare_session")
    
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'multipart/form-data; boundary=---------------------------3155108790125044357144257990',
    'Origin': 'https://gekkk.co',
    'Connection': 'keep-alive',
    'Referer': 'https://gekkk.co/',
    'Cookie': f'XSRF-TOKEN={xsrf}; brainshare_session={brain}',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    }
    

    files = {'file[]': ('lolz.png', (open('source.png', 'rb'))), #Данные для загрузки файла
             'type':'file',
             'required': '',
             'multiple': ''}
    
    
    soup = BeautifulSoup(res.text, 'lxml')
    res = soup.find_all('div', class_='container')
    resp = res[1].find('div', class_='row')
    token = resp.find('input')['value'] #Вытаскиваем токен
    captha = resp.find('div', class_='captcha-container')
    captha = captha.find('img')['src'] #Вытаскиваем ссылку на фотографию с капчей
    
    photo1 = client.get(captha).content

    with open('cap.png', 'wb') as file:
        file.write(photo1)
    
    
    id = solver.send(file='cap.png')
    os.remove('cap.png')
    time.sleep(20)
    code = solver.get_result(id) #Обработка капчи
    
    
    data = {
        '_token': str(token),
        'captcha': str(code),
        'overview':'',
        'password':'',
        'selfdestruct':'',
        'resize_width':'',
        'resize_height':'',
        'post': 'on'
    }
    
    
    result = client.post('https://gekkk.co/neo/create-post', headers=headers, data=data, files=files)
  
    print(f'Фотография загружена! Ссылка: {result.headers["location"]}') 

    client.close()
    
load_file()

