import requests
import ast
import pyautogui
import time

"""仅需修改cookie即可"""
pyautogui.PAUSE = 1
url = 'http://esop.boss.gmcc.net/esop/oneTimeCostManagement/oneTimeCostApprove/queryWaitApproveList.action'
headers = {
   "Cookie": "sna_cookie=362B6D11EA2DCE2284A75A4913A1E2E83700C3DA2A441ABF54881062B3F54657821196FDE405E7D4EF1C916EEB4D6929F2227B0450DE62EB; JSESSIONID=0000ibg854qh0zgWmJEmzpPQy7J:1a7kco5qk; rootTicket=C8F38CA96A05ABA4A736DC5B36D2FDDE860A6F00437BBF32D29946A03F9C91FEBAC7A4431598E1C6D19C57A66D9411D72B65DE86D701CA09AF8E461A53EF87E125B64FC18FB46C06F9D6601C790C84D45342BA1A2C3293EDCF07652D5514C2D4415CE8F57154813E8B565F336D7EA24AED4E4EE69E5EC28B0083590E03780EE916B2104571C4472894110FA4133807B9919FE5DEFFAA6624BF33FDD0E486FF4BD7157A230ACDA023A6EEC54FD11F6364456A25464FD57870255B11F42A0D5A430FCC0BDC07ECEBD9205A349D948385A4FFE619CF75C4E0626CD0E8F3F8450DEC4F788406CD27EEEBC785059392BF691B226245C8B0C01EF5D6B532612C817A77; loginCookie=3708EDDFABC18AC22E9CD08F247E5F0459F26C62B3970DBC15908E66EEC26C4E86CD7B9540EC759F5BDEF1A33F5760D1BE36E3298A32B0DF0E6746C6D3CD2BB435194F707A50C0D506D26F721E64365DB76F19F6B5FB95523708EDDFABC18AC26772EBD9D14431CDD62ECC2B6F66E2B9A52B19DE41C0EEDC91AF23DD70122B81A64BEEC1ED70F490; LIFE_TIME=1628832837100_240; loginTicketCookie=8C4B5E698D1620D458A988C60662A366F6E88CB5B04E4EADEA03BDA3DA9CDC5B; LOGIN_OUT_USE_LOGINID=A2EE450F683811BA3957CCB0260694CEB3E96E691418A2D9E5B180F6B18BC18CB2D1A0CC0ACC00F47D449D5B037DB54A75B0478E3B03B9A4A06F97DF9DE1551A6D91357079C547893DF55DEB3F952D0346AD3BA9E995D63D957CF9F13E9FB558; dtcqsyslocation=FEC497828E8EC12206BE9D9062C6E4704B2DDCA16262BD59458442457D802975; STAFF_LOGIN_LOG_ID=613112739; STAFF_LOGIN_TOKEN_ID=613112740; BIGipServerngesop_crm-01=!pRITKOi27h2oH6L0R1Y8/BqLjpoIcJ/zQjxXcptJnIwkyAgt5kj5DGwOlzeD35PjEhSooW4ih+SbMXg=; com.huawei.boss.CURRENT_TAB=ESOP_oneTimeCostQuery; com.huawei.boss.CURRENT_MENUID=ESOP_oneTimeCostQuery; com.huawei.boss.CURRENT_BUSIID=34fc43073d3248249cb9342a4280e230",
}
params = {
   "pageInfo.currentPage": '1',
   "pageInfo.numPerPage": '20',
   'search.region': '756',
}

click_X = 300
click_Y = 100
x = 550
y = 325
gap = 27.5

response = requests.post(url,headers=headers, params=params)
response.encoding = 'utf-8'
text = response.text
text = ast.literal_eval(text)
length = len(text['rows'])
sum = int(text['total'])
pages = 0

if sum % length != 0:
    pages = (sum // length) + 1
else:
    pages = sum // length

for page in range(1, pages+1):
    # print("第"+str(page)+"页开始截图:")
    print(page)
    params['pageInfo.currentPage'] = str(page)
    response = requests.post(url,headers=headers, params=params)
    response.encoding = 'utf-8'
    text = response.text
    text = ast.literal_eval(text)
    length = len(text['rows'])
    for i in range(length):
        name = text['rows'][i]['appName']
        pyautogui.press('end')
        pyautogui.click(x,y+(20-length+i)*gap)
        time.sleep(2)
        pyautogui.press('home')
        pyautogui.screenshot(name+"_1.png")
        pyautogui.press('end')
        pyautogui.screenshot(name+"_2.png")
        pyautogui.press('home')
        pyautogui.click(600,265)
    if page != pages:
        pyautogui.press('end')
        pyautogui.click(693,900)
        time.sleep(4)
        print("第"+str(page)+"页截图完成!")
    else:
        print("第"+str(page)+"页截图完成!")

