import requests
import ast
import calendar
import pymysql
import pyautogui
import time
import re
import os


path = "C:\\图片"
pyautogui.PAUSE = 1
url = 'http://esop.boss.gmcc.net/esop/oneTimeCostManagement/oneTimeCostApprove/queryWaitApproveList.action'
headers = {'Cookie':'local_=zh_CN; sna_cookie=38D890C50493435F2E0F820F94918D6474087129333171CA199D7DB555B0B308561578745113C52E10C2B7885C9EA3BA86850358C9AD2DFD; JSESSIONID=0000r3LW3knhoCemiZe-2q596pV:1a7kdbj6m; dtcqsyslocation=FEC497828E8EC12206BE9D9062C6E4704B2DDCA16262BD59458442457D802975; BIGipServerngesop_crm-01=!WfSCkh7BHnTbbp/0R1Y8/BqLjpoIcInVJVrOtCeTYZ2ZsJaDrCxvsd4QRvpc+3ewFf/ffqyEY0YHf4A=; rootTicket=C8F38CA96A05ABA4A736DC5B36D2FDDE860A6F00437BBF32D29946A03F9C91FEBAC7A4431598E1C6D19C57A66D9411D72B65DE86D701CA09AF8E461A53EF87E125B64FC18FB46C06F9D6601C790C84D4F8FB6B10B0119BA039828ADF9D0D2ADE0C2BE6FA6B0867FA984CEAA8FDDDE2C93292EAA97E3B1C1B2AF74177EB53620080A95060DC817E250B70F5A47E1534C4919FE5DEFFAA662406FE74F48E154D274D46F3E85DE66E013FBB88BC9817ABA936B911C455FEAC99064800A6E4B9BB5779962C11D5B373D1F7B421E48350887603F723E6453014702B3E0E9F5F9BAD3761EC0A4A6C82BBCF51ACE7851329F392AEE085360D7196C7F4E1FB291105B1D5; loginCookie=3708EDDFABC18AC22E9CD08F247E5F04B1AC5235391250AF15908E66EEC26C4E86CD7B9540EC759F5BDEF1A33F5760D1BE36E3298A32B0DF0E6746C6D3CD2BB435194F707A50C0D5CFFE0A5E3B5ECC65EAFBC448ABF4DB683708EDDFABC18AC26772EBD9D14431CDD62ECC2B6F66E2B9D3DA689DB6D8B67CC07D7A845AC43CD8A64BEEC1ED70F490; loginTicketCookie=A5BCE114E79A20EBF9909308FBE1EF95F6E88CB5B04E4EADEA03BDA3DA9CDC5B; LOGIN_OUT_USE_LOGINID=A2EE450F683811BAFF0F114F60B0CA499BCA1F91026C717378F35E5900536FEADD67FD41244BB626A8AE290DEA30A80775B0478E3B03B9A4A06F97DF9DE1551A6D91357079C547893DF55DEB3F952D0346AD3BA9E995D63D18BF012CFF334F21; STAFF_LOGIN_LOG_ID=618689140; STAFF_LOGIN_TOKEN_ID=618689141; com.huawei.boss.CURRENT_TAB=undefined; com.huawei.boss.CURRENT_MENUID=undefined; LIFE_TIME=1629958204295_240'}
params = {
   "pageInfo.currentPage": '1',
   "pageInfo.numPerPage": '20',
   'search.region': '756',
   'search.prodId':'',
   'search.startDate':'',
   "search.endDate":'',
}

MYSQL_LOCAL = {
    'host': '10.249.245.100',
    'port': 3306,
    'database': 'post_assess',
    'user': 'root',
    'password': '123456'
}

conn = pymysql.connect(host=MYSQL_LOCAL['host'], user=MYSQL_LOCAL['user'], password=MYSQL_LOCAL['password'],
                               database=MYSQL_LOCAL['database'], charset='utf8')
cursor = conn.cursor()
sql = "select product_code, out_bill_time, out_bill_money from ict_product_msg where product_code REGEXP '^[0-9]+$'"
cursor.execute(sql)
ID = list(cursor.fetchall())

if not os.path.exists(path):
    os.makedirs(path)

for i in range(len(ID)):
    data_list = []
    params['search.prodId'] = ID[i][0]
    year = int(ID[i][1][:4])
    month = int(ID[i][1][5:7])
    if month == 1:
        day = calendar.monthrange(year, month+1)[1]
        params['search.startDate'] = str(year-1) + '-' + str(12) + "-01" + " 00:00:00"
        params['search.endDate'] = str(year) + '-' + str(month+1) + '-' + str(day) + " 23:59:59"
    elif month == 12:
        day = calendar.monthrange(year, 1)[1]
        params['search.startDate'] = str(year) + '-' + str(month-1) + "-01" + " 00:00:00"
        params['search.endDate'] = str(year+1) + '-' + str(1) + '-' + str(day) + " 23:59:59"
    else:
        day = calendar.monthrange(year, month+1)[1]
        params['search.startDate'] = str(year) + '-' + str(month-1) + "-01" + " 00:00:00"
        params['search.endDate'] = str(year) + '-' + str(month+1) + '-' + str(day) + " 23:59:59"
    response = requests.post(url,headers=headers, params=params)
    response.encoding = 'utf-8'
    text = response.text
    text = ast.literal_eval(text)
    for j in text['rows']:
        if float(j['allMoney']) == float(ID[i][-1]):
            data_list.append(j)
    if len(data_list) == 0:
        pass
    else:
        for k in range(len(data_list)):
            name = data_list[k]['appId'] + "-"+data_list[k]['appName']
            id = data_list[k]['appId']
            folder_path = path+"\\"+data_list[k]['appName']+'-'+data_list[k]['custName']
            os.makedirs(folder_path)
            if i == 0 and k == 0:
                pyautogui.click(1700,100)
                pyautogui.press('end')
                pyautogui.click(1270,125)
                if id.isdigit():
                    pyautogui.typewrite(id)
                else:
                    pattern_1 = re.compile("[a-zA-Z]+")
                    pattern_2 = re.compile('[0-9]+')
                    pyautogui.typewrite(pattern_1.findall(id)[0])
                    pyautogui.press('space')
                    pyautogui.typewrite(pattern_2.findall(id)[0])
                pyautogui.click(1130, 250)
                time.sleep(1.5)
            else:
                pyautogui.press('end')
                pyautogui.click(1250,290)
                if id.isdigit():
                    pyautogui.typewrite(id)
                else:
                    pattern_1 = re.compile("[a-zA-Z]+")
                    pattern_2 = re.compile('[0-9]+')
                    pyautogui.typewrite(pattern_1.findall(id)[0])
                    pyautogui.press('space')
                    pyautogui.typewrite(pattern_2.findall(id)[0])
                pyautogui.click(1140,415)
                time.sleep(1.5)
            pyautogui.press('end')
            pyautogui.click(550, 500)
            time.sleep(2)
            pyautogui.press('home')
            pyautogui.screenshot(folder_path+"\\"+name+"_1.png")
            pyautogui.press('end')
            pyautogui.screenshot(folder_path+"\\"+name+"_2.png")
            pyautogui.press('home')
            pyautogui.click(600,265)
            pyautogui.press('end')
            pyautogui.click(1250,290)
            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
