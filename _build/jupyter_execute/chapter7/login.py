#!/usr/bin/env python
# coding: utf-8

# ## 자동 로그인

# 서버연결 및 로그인을 수행하려면 XASession 이라는 이름의 COM 클래스에 대한 객체를 선언하고 해당 객체가 제공하는 메서드를 호출해야 합니다. 아래는 서버연결 및 로그인을 차례대로 수행하는 코드입니다.

# In[ ]:


# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" #< hts:실투자, demo: 모의투자
    login_ok = False #<

    
# 실행용 클래스
class Main:
    def __init__(self):
        print("자동 로그인을 시도합니다")

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler) #<
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) # 서버 연결
        session.Login(아이디, 비밀번호, 공인인증, 0, False) # 로그인 정보 입력

        while MyObjects.login_ok is False: # 로그인 결과를 기다리는 루프
            pythoncom.PumpWaitingMessages() 


# 위 코드에서 MyObjects.server 와 MyObjects.login_ok 는 MyObjects 클래스에서 정의된 변수들입니다. 모의투자 서버에서 API 사용법을 익히기 위해 MyObjects.server 변수의 값은 'demo' 로 저장했으나, 실투자 서버를 사용을 원할 경우엔 'server' 로 저장하면 됩니다. 한편, 로그인 결과를 알기위해 MyObjects.login_ok 변수의 기본 값은 'False'로 저장하였고, 로그인 결과 메시지를 받으면 'True' 로 변경하여 위 코드의 while 문을 빠져 나옵니다.

# 다음은 로그인 결과 메시지를 받기 위한 XS_event_handler 클래스 입니다. 로그인에 성공하면 증권서버는 szCode 변수에 "0000" 값을 반환합니다. 로그인에 성공하였으므로 MyObjects.login_ok 의 값을 'True' 로 변환 합니다. 반면, 로그인이 실패 시, 'False' 값을 유지 합니다.

# In[ ]:


# 서버접속 및 로그인 요청 이후 수신결과 데이터를 다루는 구간
class XS_event_handler:

    def OnLogin(self, szCode, szMsg):
        print("%s %s" % (szCode, szMsg), flush=True)
        if szCode == "0000": # 로그인 성공
            MyObjects.login_ok = True
        else: # 로그인 실패
            MyObjects.login_ok = False


# 마지막으로 모의투자 서버 접속 시, 공동인증이 필요 없습니다. 아래 전체 코드를 실행 시키고 로그인 결과를 확인 합니다. 

# In[1]:


import win32com.client #<
import pythoncom #<

'''
로그인 하기
'''

# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" #< hts:실투자, demo: 모의투자
    login_ok = False #<


# 서버접속 및 로그인 요청 이후 수신결과 데이터를 다루는 구간
class XS_event_handler:

    def OnLogin(self, szCode, szMsg): 
        print("%s %s" % (szCode, szMsg), flush=True) 
        if szCode == "0000": 
            MyObjects.login_ok = True 
        else: 
            MyObjects.login_ok = False 

# 실행용 클래스
class Main:
    def __init__(self):
        print("자동 로그인을 시도합니다")

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler) #<
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) #< 서버 연결
        session.Login(아이디, 비밀번호, '', 0, False) #< 서버 연결

        while MyObjects.login_ok is False: #<
            pythoncom.PumpWaitingMessages() #<

if __name__ == "__main__":
    Main()

