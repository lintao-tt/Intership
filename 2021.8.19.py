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
pyautogui.click(100,100)
pyautogui.click(800,200)
pyautogui.click(800,235)
pyautogui.click(1200,475)
pyautogui.click(100,100)
time.sleep(8)
url = 'http://esop.boss.gmcc.net/esop/oneTimeCostManagement/oneTimeCostApprove/queryWaitApproveList.action'
headers = {'Cookie':'local_=zh_CN; sna_cookie=38D890C50493435F2E0F820F94918D6474087129333171CA199D7DB555B0B308561578745113C52E10C2B7885C9EA3BA86850358C9AD2DFD; dtcqsyslocation=FEC497828E8EC12206BE9D9062C6E4704B2DDCA16262BD59458442457D802975; BIGipServerngesop_crm-01=!WfSCkh7BHnTbbp/0R1Y8/BqLjpoIcInVJVrOtCeTYZ2ZsJaDrCxvsd4QRvpc+3ewFf/ffqyEY0YHf4A=; com.huawei.boss.CURRENT_TAB=undefined; com.huawei.boss.CURRENT_MENUID=undefined; JSESSIONID=0000GmjYbyBCkz4LVq7uofbEyIX:1a7kdbj6m; rootTicket=C8F38CA96A05ABA4A736DC5B36D2FDDE860A6F00437BBF32D29946A03F9C91FEBAC7A4431598E1C6D19C57A66D9411D72B65DE86D701CA09AF8E461A53EF87E125B64FC18FB46C06F9D6601C790C84D4F024340916C4A01A56E34BA6AC19D82709EF393F33B991968FC6CF77DB205F2546E711F883FFFF61B6EC6624D9F2E92C5731216C709EBD604E2EB9EEA618D44E919FE5DEFFAA66244F9C6495A83B1E8E3190F3C03758CE898154BFBFE6BCC61AFB6A0C629E25436F3CB07555929C007F68D46BE67B06A140818214A2AAB76F768FA3FA09262899EB8AE48E8F6CEB82FCBE3DA515B7DD69188BF125BF12A91CBF9CCADB1C9F3E5B7A8128BCFD799A2523; loginCookie=3708EDDFABC18AC22E9CD08F247E5F04B1AC5235391250AF15908E66EEC26C4E86CD7B9540EC759F5BDEF1A33F5760D1BE36E3298A32B0DF0E6746C6D3CD2BB435194F707A50C0D5A4BC15C22FAECAEE46C1FF9591991C463708EDDFABC18AC26772EBD9D14431CDD62ECC2B6F66E2B9D3DA689DB6D8B67C80D4F08602F44DD5A64BEEC1ED70F490; loginTicketCookie=4C575E8DF201EA974C499E2F15E47D6DF6E88CB5B04E4EADEA03BDA3DA9CDC5B; LOGIN_OUT_USE_LOGINID=A2EE450F683811BA54AA5D5AC13170DE267E0AAD5614B5C121D933D8E577B2AF7D62E928FF5C41E735B7E5496E97285475B0478E3B03B9A4A06F97DF9DE1551A6D91357079C547893DF55DEB3F952D0346AD3BA9E995D63D18BF012CFF334F21; STAFF_LOGIN_LOG_ID=618829306; STAFF_LOGIN_TOKEN_ID=618829307; LIFE_TIME=1629972762629_240'}
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
