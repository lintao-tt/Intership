import requests
import ast
import calendar
import pymysql
import pyautogui
import time
import re
import os

path = "D:\\图片"
pyautogui.PAUSE = 1
url = 'http://esop.boss.gmcc.net/esop/oneTimeCostManagement/oneTimeCostApprove/queryWaitApproveList.action'
headers = {'Cookie':'sna_cookie=CD568329685C849248767283EC0DBBCD6E7DE2A0D7B585BCC0E28526BEB7A63E4BFAB53168DC2DD3CA58043DFA196F811FF2B1E7AE9D84CF; JSESSIONID=0000i9-31Yxb55k9VIoWwEzxFSX:1bkroenlf; rootTicket=C8F38CA96A05ABA4A736DC5B36D2FDDE860A6F00437BBF32D29946A03F9C91FEBAC7A4431598E1C6D19C57A66D9411D72B65DE86D701CA09AF8E461A53EF87E125B64FC18FB46C06F9D6601C790C84D4A7029DC40750AC9081EE117C63B70F9C18B083CC3230C4C72613C053FDF8239ECC3DD028ABA97ACC29A0E87701E00225BE50D25F6680ABDCC13911992750C754919FE5DEFFAA66245220F76E89C7B00B040B6485A80AB03D96367D744CB4ACAA56B5849B2706EC776F4853516D7377736B9EBE4C10AB4DF1067BAE22D1A6C2519A7B17285BBE59D1F2AF32A997C9753EDE3978BE40582CCB0FC69C1AAA06F37594A657B12FE2ABEA6822EE88FB2F3E78; loginCookie=3708EDDFABC18AC22E9CD08F247E5F0459F26C62B3970DBC15908E66EEC26C4E86CD7B9540EC759F5BDEF1A33F5760D1BE36E3298A32B0DF0E6746C6D3CD2BB435194F707A50C0D56F90816B092627FE1B3F6859BA057F0A3708EDDFABC18AC26772EBD9D14431CDD62ECC2B6F66E2B9B41FC3A721D91B70711C96C644919A60A64BEEC1ED70F490; LIFE_TIME=1629454793156_240; loginTicketCookie=B3623885E4D663CD69E068664333EC97F6E88CB5B04E4EADEA03BDA3DA9CDC5B; LOGIN_OUT_USE_LOGINID=A2EE450F683811BA436F2312883D2A97A6E54760F7F2A1D0142E22BDF01153D3D4F7A9304C89F4B99C4869313F70047175B0478E3B03B9A4A06F97DF9DE1551A6D91357079C547893DF55DEB3F952D0346AD3BA9E995D63D957CF9F13E9FB558; dtcqsyslocation=FEC497828E8EC12206BE9D9062C6E4704B2DDCA16262BD59458442457D802975; STAFF_LOGIN_LOG_ID=616211105; STAFF_LOGIN_TOKEN_ID=616211106; BIGipServerngesop_crm-01=!4G4G67JKlkDYrID0R1Y8/BqLjpoIcFNbrZJ3tsBQxW9UlYjwp5mrZ+JLE4IeFyKa9vAsTDJ8cxfCQPg=; com.huawei.boss.CURRENT_TAB=ESOP_oneTimeCostQuery; com.huawei.boss.CURRENT_MENUID=ESOP_oneTimeCostQuery; com.huawei.boss.CURRENT_BUSIID=04f8f76d09d54158a3bd3864ad1b7dbb'}
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

if not os.exists(path):
    os.makedirs(path)

for i in range(len(ID)):
    data_list = []
    params['search.prodId'] = ID[i][0]
    year = int(ID[i][1][:4])
    month = int(ID[i][1][5:7])
    if month == 1:
        day = calendar._monthlen(year, month+1)
        params['search.startDate'] = str(year-1) + '-' + str(12) + "-01" + " 00:00:00"
        params['search.endDate'] = str(year) + '-' + str(month+1) + '-' + str(day) + " 23:59:59"
    elif month == 12:
        day = calendar._monthlen(year, 1)
        params['search.startDate'] = str(year) + '-' + str(month-1) + "-01" + " 00:00:00"
        params['search.endDate'] = str(year+1) + '-' + str(1) + '-' + str(day) + " 23:59:59"
    else:
        day = calendar._monthlen(year, month+1)
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
