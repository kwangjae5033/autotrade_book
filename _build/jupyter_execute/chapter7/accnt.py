#!/usr/bin/env python
# coding: utf-8

# ## 계좌 정보 조회

# XAQuery 클래스를 사용하면 게좌 잔고 내역을 조회 할 수 있습니다. XAQuery는 크게 총 세 단계로 나눌 수 있습니다. <br>
# <ol>
#   <li>XQuery 클래스 객체 선언 및 Res 파일 등록</li>
#   <li>해당 XQuery 입력 변수 설정 및 요청</li>
#   <li>XQuery 요청 데이터 수신</li>
# </ol>

# 첫 단계는 XQuery 클래스 객체를 선언하고 계좌 잔고 조회용 Res 파일을 등록합니다. DevCenter의 TR 목록에서 "주식잔고2"를 통해 계좌 정보를 조회 할 수 있으므로 t0424.res 파일을 등록해 줍니다.

# In[ ]:


# XQuery 클래스 객체 선언 및 계좌 잔고 조회 Res 파일 등록

MyObjects.tr_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
MyObjects.tr_event.ResFileName = "C:/eBEST/xingAPI/Res/t0424.res"


# 두 번째 단계에서는 먼저 해당 XQuery의 입력 변수를 SetFieldData() 함수를 통해 설정합니다. 그 다음으로 요청 함수 t0424_request() 를 호출합니다. 

# In[ ]:


# MyObjects 클래스에 새로 추가된 변수: acc_num, acc_pw, t0424_dict, t0424_request 

class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    acc_num = 계좌번호 #< 계좌번호
    acc_pw = 계좌비밀번호 #< 계좌비밀번호

    t0424_dict = {} #< 잔고내역2 종목들 모아 놓은 딕셔너리

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보

    t0424_request = None #< 잔고내역2 조회 요청함수
    ##################


# 해당 XQuery 입력 변수 설정

def t0424_request(self, cts_expcode=None, next=None): 

    time.sleep(1.1) 

    MyObjects.tr_event.SetFieldData("t0424InBlock", "accno", 0, MyObjects.acc_num) # 계좌번호
    MyObjects.tr_event.SetFieldData("t0424InBlock", "passwd", 0, MyObjects.acc_pw) # 계좌 비밀번호
    MyObjects.tr_event.SetFieldData("t0424InBlock", "prcgb", 0, "1") # 단가구분; 1:평균단가, 2:BEP단가
    MyObjects.tr_event.SetFieldData("t0424InBlock", "chegb", 0, "2") # 체결구분; 0:결제기준잔고. 2:체결기준(잔고가 0이 아닌 종목만 조회)
    MyObjects.tr_event.SetFieldData("t0424InBlock", "dangb", 0, "0") # 단일가구분; 0:정규장, 1:시간외단일가
    MyObjects.tr_event.SetFieldData("t0424InBlock", "charge", 0, "1") # 제비용포함여부; 0:제비용미포함, 1:제비용포함
    MyObjects.tr_event.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode) # 처음조회시는 Space, 연속조회시에 이전 조회한 OutBlock의 cts_expcode 값으로 설정

    MyObjects.tr_event.Request(next) 

    MyObjects.tr_ok = False
    while MyObjects.tr_ok is False: 
        pythoncom.PumpWaitingMessages()


# 요청 함수 호출

MyObjects.t0424_request = self.t0424_request
MyObjects.t0424_request(cts_expcode="", next=False)


# 마지막 세 번째 단계에서는 XQuery 로 요청한 데이터를 수신하는 클래스를 생성 합니다. 'code' 변수를 통해 요청했던 데이터를 구분하고 GetFieldData() 함수를 통해 계좌 정보를 조회 할 수 있습니다. . 

# In[ ]:


# TR 요청 이후 수신결과 데이터를 다루는 구간

class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)

        if code == "t0424": 

            cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0) 

            occurs_count = self.GetBlockCount("t0424OutBlock1") 
            for i in range(occurs_count): 
                expcode = self.GetFieldData("t0424OutBlock1", "expcode", i) 

                if expcode not in MyObjects.t0424_dict.keys(): 
                    MyObjects.t0424_dict[expcode] = {} 

                tt = MyObjects.t0424_dict[expcode] 
                tt["잔고수량"] = int(self.GetFieldData("t0424OutBlock1", "janqty", i)) 
                tt["매도가능수량"] = int(self.GetFieldData("t0424OutBlock1", "mdposqt", i)) 
                tt["평균단가"] = int(self.GetFieldData("t0424OutBlock1", "pamt", i)) 
                tt["종목명"] = self.GetFieldData("t0424OutBlock1", "hname", i) 
                tt["종목구분"] = self.GetFieldData("t0424OutBlock1", "jonggb", i)  
                tt["수익률"] = float(self.GetFieldData("t0424OutBlock1", "sunikrt", i)) 

                print("잔고내역 %s" % tt, flush=True)

            # 과거 데이터를 더 가져오고 싶을 때는 연속조회를 해야한다.
            if self.IsNext is True: #< 과거 데이터가 더 존재한다.
                MyObjects.t0424_request(cts_expcode=cts_expcode, next=self.IsNext) 
            elif self.IsNext is False: 
                MyObjects.tr_ok = True 

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("systemError: %s, messageCode: %s, message: %s" % (systemError, messageCode, message), flush=True)


# 아래 전체 코드를 실행하고 계좌 정보 조회 결과를 확인 합니다.

# In[4]:


import win32com.client
import pythoncom
import time

'''
잔고내역 가져오기
'''

# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
    server = "demo" # hts:실투자, demo: 모의투자
    tr_ok = False # TR요청
    acc_num = 계좌번호 #< 계좌번호
    acc_pw = 계좌비밀번호 #< 계좌비밀번호

    t8436_list = [] # 종목코드 모아놓는 리스트
    t0424_dict = {} #< 잔고내역2 종목들 모아 놓은 딕셔너리

    ####### 요청 함수 모음
    tr_event = None # TR요청에 대한 API 정보

    t0424_request = None #< 잔고내역2 조회 요청함수
    ##################

# 실시간으로 수신받는 데이터를 다루는 구간
class XR_event_handler:
    pass

# TR 요청 이후 수신결과 데이터를 다루는 구간
class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)

        if code == "t0424": #<

            cts_expcode = self.GetFieldData("t0424OutBlock", "cts_expcode", 0) #<

            occurs_count = self.GetBlockCount("t0424OutBlock1") #<
            for i in range(occurs_count): #<
                expcode = self.GetFieldData("t0424OutBlock1", "expcode", i) #<

                if expcode not in MyObjects.t0424_dict.keys(): #<
                    MyObjects.t0424_dict[expcode] = {} #<

                tt = MyObjects.t0424_dict[expcode] #<
                tt["잔고수량"] = int(self.GetFieldData("t0424OutBlock1", "janqty", i)) #<
                tt["매도가능수량"] = int(self.GetFieldData("t0424OutBlock1", "mdposqt", i)) #<
                tt["평균단가"] = int(self.GetFieldData("t0424OutBlock1", "pamt", i)) #<
                tt["종목명"] = self.GetFieldData("t0424OutBlock1", "hname", i) #<
                tt["종목구분"] = self.GetFieldData("t0424OutBlock1", "jonggb", i)  #<
                tt["수익률"] = float(self.GetFieldData("t0424OutBlock1", "sunikrt", i)) #<

                print("잔고내역 %s" % tt, flush=True)

            # 과거 데이터를 더 가져오고 싶을 때는 연속조회를 해야한다.
            if self.IsNext is True: #< 과거 데이터가 더 존재한다.
                MyObjects.t0424_request(cts_expcode=cts_expcode, next=self.IsNext) #<
            elif self.IsNext is False: #<
                MyObjects.tr_ok = True #<

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("systemError: %s, messageCode: %s, message: %s" % (systemError, messageCode, message), flush=True)

# 서버접속 및 로그인 요청 이후 수신결과 데이터를 다루는 구간
class XS_event_handler:

    def OnLogin(self, szCode, szMsg):
        print("%s %s" % (szCode, szMsg), flush=True)
        if szCode == "0000":
            MyObjects.tr_ok = True
        else:
            MyObjects.tr_ok = False

# 실행용 클래스
class Main:
    def __init__(self):
        print("실행용 클래스이다")

        session = win32com.client.DispatchWithEvents("XA_Session.XASession", XS_event_handler)
        session.ConnectServer(MyObjects.server + ".ebestsec.co.kr", 20001) # 서버 연결
        session.Login(아이디, 비밀번호, 공인인증, 0, False) # 서버 연결

        while MyObjects.tr_ok is False:
            pythoncom.PumpWaitingMessages()

        MyObjects.tr_event = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XQ_event_handler)
        MyObjects.tr_event.ResFileName = "C:/eBEST/xingAPI/Res/t0424.res"
        MyObjects.t0424_request = self.t0424_request
        MyObjects.t0424_request(cts_expcode="", next=False)

    def t0424_request(self, cts_expcode=None, next=None): #<

        time.sleep(1.1) #<

        MyObjects.tr_event.SetFieldData("t0424InBlock", "accno", 0, MyObjects.acc_num) #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "passwd", 0, MyObjects.acc_pw) #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "prcgb", 0, "1") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "chegb", 0, "2") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "dangb", 0, "0") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "charge", 0, "1") #<
        MyObjects.tr_event.SetFieldData("t0424InBlock", "cts_expcode", 0, cts_expcode) #<

        MyObjects.tr_event.Request(next) #<

        MyObjects.tr_ok = False #<
        while MyObjects.tr_ok is False: #<
            pythoncom.PumpWaitingMessages() #<

if __name__ == "__main__":
    Main()

