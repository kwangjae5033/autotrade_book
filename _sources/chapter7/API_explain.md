# API 작동 방식

## xingAPI 이란?

xingAPI 는 주식, 선물옵션, 야간 선물옵션, 해외선물, FX마진 등 주요 상품을 모두 거래 할 수 있습니다.
빠른 시세는 물론, 다양한 데이터 (종목마스터, 투자정보, 주문, 잔고 등)를 HTS 와 동일하게 제공합니다.
이베스트투자증권은 DevCenter 를 통해 API 양식을 쉽게 설명하고 있습니다. 
xingAPI 를 통해 조회 할 수 있는 TR 및 Real 목록 검색이 가능하고, 필드와 속성을 간편하게 확인할 수 있습니다.
더 나아가, TR 및 Real 조회 테스트 기능이 있어서 정확하고 효율적으로 코드 작성을 진행 할 수 있습니다. 
DevCenter 에 관한 활용 방법 및 조회 테스트는 많은 자료에서 소개되고 있으므로 생략하겠습니다. <br>

xingAPI 는 아래 Table 과 같이 크게 세 가지 클래스를 제공합니다.

```{list-table}
:header-rows: 1

* - 객체명
  - 설명
  - 파일명
* - XASession
  - 서버연결, 로그인 등
  - XA_Session.dll
* - XAQuery
  - 조회TR
  - XA_DataSet.dll
* - XAReal
  - 실시간TR
  - XA_DataSet.dll
```

xingAPI 는 COM 버전이지만 DLL 파일을 사용합니다. DLL 은 Dynamic Link Library의 약자이며 xingAPI 에서 제공하는
통신 모듈 프로그램 코드가 들어있습니다. 아래 Fig 1 처럼 증권사 서버와 사용자 프로그램 코드의 통신을 연결해 줍니다.

```{figure} images/API_explain_1.png
:width: 800px
:height: 400px
:name: API 작동 방식

COM 버전 DLL 버전
```

*아래 도표 다시 그리고 설명 추가*


```{figure} images/API_explain_2.png
:width: 800px
:height: 400px
:name: API 작동 방식

xingAPI 프로세스 순서
```

*API를 활용한 코드 설명 추가*

 1. 변수를 관리하는 MyObjects 클래스
 2. 데이터를 요청하는 Main 클래스
 3. 데이터를 수신하는 XQ_event_handler 클래스

'''
매수/매도 주문 넣기
'''

import win32com.client
import pythoncom
import time
import threading
import pandas as pd

# 앞으로 사용하게 될 변수들을 모아 놓는다.
class MyObjects:
 

# 실시간으로 수신받는 데이터를 다루는 구간
class XR_event_handler:

    def OnReceiveRealData(self, code):

       
# TR 요청 이후 수신결과 데이터를 다루는 구간
class XQ_event_handler:

    def OnReceiveData(self, code):
        print("%s 수신" % code, flush=True)

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


if __name__ == "__main__":
    Main()
    