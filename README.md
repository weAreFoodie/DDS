# DDS
## 개요
WebSocket을 통해 실시간 주가 데이터를 안정적으로 수집하고 ELK 스택을 통해 실시간 데이터 처리 및 분석 과 효율적 데이터 관리를 학습하고자 프로젝트를 구성했습니다.

단기 데이터는 Elasticsearch에 저장하여 빠른 검색과 시각화를 지원하고
요약 데이터를 MySQL에 저장하여 장기 데이터 분석 및 백업을 관리할 수 있도록 아키텍쳐를 설계했습니다.

---
## 팀원
<table>
  <tbody>
    <tr>
      <td align="center">
         <a href="https://github.com/danidana2">
          <img src="https://avatars.githubusercontent.com/u/150885774?v=4" width="150px;" alt=""/>
          <br /><sub><b> 최다영 </b></sub>
        </a>
        <br />
      </td>
      <td align="center">
          <a href="https://github.com/dyoun12">
          <img src="https://avatars.githubusercontent.com/u/107902336?v=4" width="150px;" alt=""/>
          <br /><sub><b> 김대연 </b></sub>
        </a>
        <br />
      </td>
      <td align="center">
        <a href="https://github.com/min-jp">
          <img src="https://avatars.githubusercontent.com/u/129049084?v=4" width="150px;" alt=""/>
          <br /><sub><b> 민정인 </b></sub>
        </a>
        <br />
      </td>
      <td align="center">
        <a href="https://github.com/EOTAEGYU">
          <img src="https://avatars.githubusercontent.com/u/123963462?v=4" width="150px;" alt=""/>
          <br /><sub><b> 어태규 </b></sub>
        </a>
        <br />
      </td>
    </tr>
  </tbody>
</table>

---
## 활용 기술

<img src="https://img.shields.io/badge/Filebeat-DD002A?style=for-the-badge&logo=elastic&logoColor=white" alt="Filebeat"> <img src="https://img.shields.io/badge/Logstash-005571?style=for-the-badge&logo=elastic&logoColor=white" alt="Logstash"> <img src="https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch"> <img src="https://img.shields.io/badge/Kibana-FF69B4?style=for-the-badge&logo=kibana&logoColor=white" alt="Kibana"> <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL"> <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white" alt="Ubuntu"> <img src="https://img.shields.io/badge/WebSocket-004A59?style=for-the-badge&logo=websocket&logoColor=white" alt="WebSocket"> <img src="https://img.shields.io/badge/DBeaver-372923?style=for-the-badge&logo=dbeaver&logoColor=white" alt="DBeaver"> <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"> <img src="https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white" alt="Slack"> <img src="https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white" alt="Notion">

--- 


## 아키텍처
<img width="3280" alt="Untitled (1)" src="https://github.com/user-attachments/assets/499adbba-694b-4576-a87a-de47fe9d6a5d" />

| name  | FileBeat | Logstash | Elasticsearch | Kibana | Mysql | Ubuntu |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| version | 7.11.1 | 7.11.1 | 7.11.1 | 7.11.1 | 7.11.1 | 7.11.1 |

---

## 데이터 구조
### ElasticSearch
|Element|**한글명**|Type|
|---|---|---|
|MKSC_SHRN_ISCD|유가증권 단축 종목코드|text|
|STCK_CNTG_HOUR|주식 체결 시간|date|
|STCK_PRPR|주식 현재가|long|
|CNTG_VOL|체결 거래량|long|
|ACML_VOL|누적 거래량|long|
|STCK_HGPR|주식 최고가|long|
|STCK_LWPR|주식 최저가|long|

## 데이터 흐름
### 1. 한국 투자 증권 API를 사용
- 삼성전자(005930)의 실시간 데이터를 1초마다 받아와 csv에 저장
**CSV 저장 예시**
- 유가증권 단축 종목코드, 주식 체결 시간, 주식 현재가, 체결 거래량, 누적 거래량, 주식 최고가, 주식 최저가
![Pasted image 20250121165626](https://github.com/user-attachments/assets/b6ae6624-76d6-4391-9bcd-75d06e3e2a68)


## 2. filebeat로 csv 파일 읽어오기
- path:에 실시간으로 저장되고 있는 csv 파일 경로 지정
```yml
 paths:
    C:\00.dataSet\stock.csv
```
- output을 logstash로 설정
```yml
output.logstash:
  hosts: ["localhost:5044"]
```

## 3. logstash로 전처리 후 elelasticsearch에 저장하기

### 3-1. message 필드를 ',' 분할하여 새로운 필드로 추가
```yml
filter {
  mutate {
    # "message" 필드를 ','로 분할하여 새로운 필드로 추가
    split => [ "message", "," ]
    add_field => {
      "MKSC_SHRN_ISCD" => "%{[message][0]}"
      "STCK_CNTG_HOUR" => "%{[message][1]}"
      "STCK_PRPR" => "%{[message][2]}"
      "CNTG_VOL" => "%{[message][3]}"
      "ACML_VOL" => "%{[message][4]}"
      "STCK_HGPR" => "%{[message][5]}"
      "STCK_LWPR" => "%{[message][6]}"
    }
  }
  ```

### 3-1. elelasticsearch 형식에 맞는 date 타입으로 변환
- 한국 투자 증권에서 제공하는 주식 체결 시간이 string 타입으로 "142011"(시간:분:초)로 들어오고 있음음
- ruby를 사용하여 현재 날짜를 가져오고 string 타입을 hh:mm:ss 형식으로 변환 후 현재 날짜와 합쳐 필드에 추가
```yml
 ruby {
    code => '
      cntg_hour = event.get("STCK_CNTG_HOUR")
      if cntg_hour
        # 현재 날짜 가져오기
        today = Time.now.strftime("%Y-%m-%d")
        # STCK_CNTG_HOUR 값을 HH:mm:ss 형식으로 변환
        formatted_time = cntg_hour.scan(/../).join(":")
        # 최종 날짜와 시간 형식으로 합치기
        full_datetime = "#{today} #{formatted_time}"
        event.set("STCK_CNTG_HOUR", full_datetime)
      end
    '
  }

  date {
    match => [ "STCK_CNTG_HOUR", "yyyy-MM-dd HH:mm:ss" ]
    timezone => "Asia/Seoul"
    target => "STCK_CNTG_HOUR"
  }
```

### 3-3. 데이터 타입 변경 및 사용하지 않는 필드 삭제
- 주식 현재가, 체결 거래량, 누적 거래량, 주식 최고가, 주식 최저가 integer로 변경
- "ecs", "host", "@version", "agent", "log", "input", "message", "@timestamp" 필드 삭제

```
   # Kibana에서 데이터 분석시 필요하기 때문에 숫자 타입으로 변경
  mutate {
    convert => {
      "STCK_PRPR" => "integer"
      "CNTG_VOL" => "integer"
      "ACML_VOL" => "integer"
      "STCK_HGPR" => "integer"
      "STCK_LWPR" => "integer"
    }
  }

  mutate {
    remove_field => ["ecs", "host", "@version", "agent", "log", "input", "message", "@timestamp"]
  }
}
```

### 3-4. elelasticsearch에 stock index로 저장
```yml
output {
  stdout {
    codec => rubydebug
  }

  elasticsearch {
    hosts => ["http://localhost:9200"]
    index => "stock"
  }
}
```

### **Elasticsearch Multi-head에서 데이터 확인**
![Pasted image 20250121172141](https://github.com/user-attachments/assets/99a904ae-c1ad-4ba2-89a7-527e6cc26890)


### Mysql
![stock - kr_stock_trade](https://github.com/user-attachments/assets/5ba73d83-be57-44c4-a399-f2289e9cd4d2)

---

## 시연

--- 

## Troubleshooting

### Logstash 인스턴스 2개 실행 중 문제

### STCK_CNTG_HOUR값 mysql 이관 중 타입 오류

DATETIME 포멧에 지원하지 않는 표현식으로 인한 예외 발생

---

## 회고
