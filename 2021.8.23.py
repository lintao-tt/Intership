from selenium import webdriver
import js2py
import time
import pyautogui

pyautogui.PAUSE = 1
"""
driver = webdriver.Chrome(r"E:\大学\实习\chromedriver.exe")
# driver.get("https://ng4a.gmcc.net/iga/login_gd.html")
driver.get("https://www.baidu.com/")
driver.maximize_window()
driver.find_element_by_class_name("s_ipt").send_keys("天猫")
driver.find_element_by_id("su").click()
driver.find_element_by_css_selector("ec-pc_comp_d20_title-text c-color-link").click()


driver.find_element_by_id("user_sms").send_keys("dingqirui")
driver.find_element_by_id("token_sms").send_keys("Dqr!23456")
driver.find_element_by_id("sendSms_btn").click()
time.sleep(10)
driver.find_element_by_id("login_btn").click()

driver.find_element_by_class_name("up_nav_text").click()
driver.find_element_by_class_name("up_nav_item allresources selected").click()




pyautogui.click(100,900)
# pyautogui.press(['ctrl', 'shift', 'I'])
# time.sleep(5)
pyautogui.click(1330, 380)
time.sleep(2)
pyautogui.press("f12")
# pyautogui.press("shift")
pyautogui.click(500,130)
time.sleep(15)
pyautogui.typewrite("document.getElementById('client_c930f75e6cfd40de875430ae2843fafa').selectedIndex=1")
pyautogui.press("enter")
# pyautogui.click(button='right')
# pyautogui.click(100,890)




# 搜索ESOP
pyautogui.click(300,245)
pyautogui.typewrite("ESOP")
pyautogui.press("enter")
time.sleep(2)


pyautogui.click(100,900)
pyautogui.click(1330, 380)
# pyautogui.click(1330, 380)
time.sleep(2)
# pyautogui.click(1330, 370)

pyautogui.click(1330, 420)
"""
dict = ast.literal_eval(dict)
headers = {'Cookie':''}
cookie = ""
for key, value in dict.items():
    cookie += key+"="+value+";"
print(cookie)
headers['Cookie'] = cookie