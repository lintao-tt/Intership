# 注意:
### 1.需在已打开一个全屏网页的情况下执行程序
### 2.在for k in ...这个循环中，if存在一个缺陷：当第一条读取数据没有查出对应的编号，程序会走else部分导致整个程序错乱(出现概率低)
### 3.程序中所设定等待时间需根据当前网络状况和电脑管家进行调整(无法登录ESOP系统则需对电脑管家进行管理)
### 4.由于无法获取每个对话框的有效时间，为避免等待元素超时，需尽快操作
### 5.当前电脑输入法需设置为中文输入法
### 6.所需的Python第三方库支持：requests、ast、calendar、pymysql、pyautogui、time、re、os
### 7.当前测试样机屏幕参数：15.6寸，1920x1080
### 8.执行程序时需将登陆过系统所保存的登录信息进行清除
### 9.切换到IE时可能出现无法点击的情况(RPA不支持IE)，可能需要人工介入
