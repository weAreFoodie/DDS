import sys
import time
import os
from dotenv import load_dotenv
import csv

import json
import requests
import asyncio
import traceback
import websockets

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode


# 데이터 추가 함수
def add_to_csv(file_name, data, headers=None):
    # 파일이 이미 존재하는지 확인
    # file_exists = os.path.exists(file_name)

    # 파일 열기 (추가 모드)
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # 파일이 존재하지 않으면 헤더 추가
        # if not file_exists and headers:
        #     writer.writerow(headers)
        
        # 데이터 추가
        writer.writerow(data)

# AES256 DECODE
def aes_cbc_base64_dec(key, iv, cipher_text):
    """
    :param key:  str type AES256 secret key value
    :param iv: str type AES256 Initialize Vector
    :param cipher_text: Base64 encoded AES256 str
    :return: Base64-AES256 decodec str
    """
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv.encode('utf-8'))
    return bytes.decode(unpad(cipher.decrypt(b64decode(cipher_text)), AES.block_size))


# 웹소켓 접속키 발급
def get_approval(key, secret):
    # url = https://openapivts.koreainvestment.com:29443' # 모의투자계좌     
    url = 'https://openapi.koreainvestment.com:9443' # 실전투자계좌
    headers = {"content-type": "application/json"}
    body = {"grant_type": "client_credentials",
            "appkey": key,
            "secretkey": secret}
    PATH = "oauth2/Approval"
    URL = f"{url}/{PATH}"
    time.sleep(0.05)
    res = requests.post(URL, headers=headers, data=json.dumps(body))
    approval_key = res.json()["approval_key"]
    return approval_key

### 1-1. 국내주식 ###

# 국내주식체결처리 출력라이브러리
def stockspurchase_domestic(data_cnt, data):
    menulist = "유가증권단축종목코드|주식체결시간|주식현재가|전일대비부호|전일대비|전일대비율|가중평균주식가격|주식시가|주식최고가|주식최저가|매도호가1|매수호가1|체결거래량|누적거래량|누적거래대금|매도체결건수|매수체결건수|순매수체결건수|체결강도|총매도수량|총매수수량|체결구분|매수비율|전일거래량대비등락율|시가시간|시가대비구분|시가대비|최고가시간|고가대비구분|고가대비|최저가시간|저가대비구분|저가대비|영업일자|신장운영구분코드|거래정지여부|매도호가잔량|매수호가잔량|총매도호가잔량|총매수호가잔량|거래량회전율|전일동시간누적거래량|전일동시간누적거래량비율|시간구분코드|임의종료구분코드|정적VI발동기준가"


    file_path = os.environ.get("FILE_PATH")
    # headers = [
    #     menulist.split('|')[0],
    #     menulist.split('|')[1],
    #     menulist.split('|')[2],
    #     menulist.split('|')[12],
    #     menulist.split('|')[13],
    #     menulist.split('|')[8],
    #     menulist.split('|')[9]
    # ]
    row = [
        data.split('^')[0],
        data.split('^')[1],
        data.split('^')[2],
        data.split('^')[12],
        data.split('^')[13],
        data.split('^')[8],
        data.split('^')[9]
    ]
    
    # 행 추가 실행
    # add_to_csv(file_path, row, headers)
    add_to_csv(file_path, row)

async def connect():
    try:
        g_appkey = os.environ.get("APP_KEY")
        g_appsecret = os.environ.get("SECERET_KEY")

        g_approval_key = get_approval(g_appkey, g_appsecret)

        url = 'ws://ops.koreainvestment.com:21000'

        # 원하는 호출을 [tr_type, tr_id, tr_key] 순서대로 리스트 만들기
        code_list = [['1','H0STCNT0','005930']]

        senddata_list=[]

        for i,j,k in code_list:
            temp = '{"header":{"approval_key": "%s","custtype":"P","tr_type":"%s","content-type":"utf-8"},"body":{"input":{"tr_id":"%s","tr_key":"%s"}}}'%(g_approval_key,i,j,k)
            senddata_list.append(temp)

        async with websockets.connect(url, ping_interval=None) as websocket:
            for senddata in senddata_list:
                await websocket.send(senddata)
                await asyncio.sleep(0.5)
                print(f"Input Command is :{senddata}")

            while True:
                data = await websocket.recv()
                # await asyncio.sleep(0.5)
                if data[0] == '0':
                    recvstr = data.split('|')
                    trid0 = recvstr[1]

                    if trid0 == "H0STCNT0":  # 주식체결 데이터 처리
                        print(os.environ.get("FILE_PATH"))
                        data_cnt = int(recvstr[2])
                        stockspurchase_domestic(data_cnt, recvstr[3])
                        await asyncio.sleep(1.0)

                elif data[0] == '1':
                    recvstr = data.split('|')
                    trid0 = recvstr[1]

                else:
                    jsonObject = json.loads(data)
                    trid = jsonObject["header"]["tr_id"]

                    if trid != "PINGPONG":
                        rt_cd = jsonObject["body"]["rt_cd"]

                        if rt_cd == '1':  # 에러일 경우 처리
                            
                            if jsonObject["body"]["msg1"] != 'ALREADY IN SUBSCRIBE':
                                print("### ERROR RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))
                            break

                        elif rt_cd == '0':  # 정상일 경우 처리
                            print("### RETURN CODE [ %s ][ %s ] MSG [ %s ]" % (jsonObject["header"]["tr_key"], rt_cd, jsonObject["body"]["msg1"]))

                            # 체결통보 처리를 위한 AES256 KEY, IV 처리 단계
                            if trid == "H0STCNI0" or trid == "H0STCNI9": # 국내주식
                                aes_key = jsonObject["body"]["output"]["key"]
                                aes_iv = jsonObject["body"]["output"]["iv"]
                                print("### TRID [%s] KEY[%s] IV[%s]" % (trid, aes_key, aes_iv))

                    elif trid == "PINGPONG":
                        print("### RECV [PINGPONG] [%s]" % (data))
                        await websocket.pong(data)
                        print("### SEND [PINGPONG] [%s]" % (data))

    # 모든 함수의 공통 부분(Exception 처리)
    except Exception as e:
        print('Exception Raised!')
        print(e)
        print('Connect Again!')
        time.sleep(0.1)

        # 웹소켓 다시 시작
        await connect()     
                    
async def main():
    try:
        # .env 로드
        load_dotenv("./.env")
        
        # 웹소켓 시작
        await connect()

    except Exception as e:
        print('Exception Raised!')
        print(e)
        
if __name__ == "__main__":
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        print("KeyboardInterrupt Exception 발생!")
        print(traceback.format_exc())
        sys.exit(-100)

    except Exception:
        print("Exception 발생!")
        print(traceback.format_exc())
        sys.exit(-200)