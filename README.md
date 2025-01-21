# DDS
## 개요
### 목적
> 1. 실시간 데이터를 이용한 ELK-Stack 활용
> 2. RDBMS 연동을 통한 데이터 보존 전략에 대한 고찰

WebSocket을 통해 실시간 주가 데이터를 안정적으로 수집하고 ELK 스택을 통해 실시간 데이터 처리 및 분석하고, 효율적인 데이터 관리를 학습하고자 프로젝트를 구성했습니다.

### 주가 데이터 선택 이유
ELK-Stack의 최대 장점인 실시간, 대용량 데이터 처리와 더불어 시각화할 수 있는 도메인을 추려보다가 해당 조건을 만족할 수 있는 국내 주식의 주가 체결 정보를 선택하게 되었습니다. 

실시간으로 추가되는 데이터와 히스토리 추적을 위한 데이터의 목적을 구분하여 
단기 데이터는 Elasticsearch에 저장하여 빠른 검색과 시각화를 지원하고
히스토리 추적을 위한 요약 데이터는 MySQL로 이관, 저장하여 장기 데이터 분석 및 백업을 관리할 수 있도록 아키텍쳐를 설계했습니다.

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

| 분류              | 로고                                                                                                                                                                              |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 데이터 처리 및 분석 | ![Filebeat](https://img.shields.io/badge/Filebeat-DD002A?style=for-the-badge&logo=elastic&logoColor=white) ![Logstash](https://img.shields.io/badge/Logstash-005571?style=for-the-badge&logo=elastic&logoColor=white) ![Elasticsearch](https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white) ![Kibana](https://img.shields.io/badge/Kibana-FF69B4?style=for-the-badge&logo=kibana&logoColor=white) ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) |
| 시스템 환경       | ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![WebSocket](https://img.shields.io/badge/WebSocket-004A59?style=for-the-badge&logo=websocket&logoColor=white)                                           |
| 개발 도구         | ![DBeaver](https://img.shields.io/badge/DBeaver-372923?style=for-the-badge&logo=dbeaver&logoColor=white)                                                 |
| 협업 툴           | ![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)   ![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white) ![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white)                                                  |

--- 


## 아키텍처
<img width="3296" alt="Untitled-찐막" src="https://github.com/user-attachments/assets/5131a0aa-d10c-4167-b816-8449d10a2047" />


| name  | FileBeat | Logstash | Elasticsearch | Kibana | Mysql | Ubuntu |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| version | 7.11.1 | 7.11.1 | 7.11.1 | 7.11.1 | 8.0.40 | 24.04.1 |

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

### Mysql
![stock - kr_stock_trade](https://github.com/user-attachments/assets/5ba73d83-be57-44c4-a399-f2289e9cd4d2)

---

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

## 4. elastic search 데이터를 logstash를 이용해 mysql에 저장하기

### 📥 4-1. `logstash-output-jdbc` 플러그인 설치

- **CMD 창에서 설치**
    1. **CMD(명령 프롬프트)** 실행
    2. Logstash가 설치된 폴더로 이동<br/>
    예: `cd C:\logstash`
    3. 아래 명령어 실행하여 플러그인 설치
        
        ```bash
        bin\logstash-plugin install logstash-output-jdbc
        ```
        
- **설치 완료 후 화면**
    
    ![image](https://github.com/user-attachments/assets/f1dfb5e0-ae96-4af0-92b9-b1346e7ef537)
    
-  **플러그인 설치 확인**
    
    Logstash가 설치된 폴더 하위 `vendor\bundle\jruby\2.5.0\gems` 폴더 내 `logstash-output-jdbc`가 존재하는지 확인
    
    ![image2](https://github.com/user-attachments/assets/34088867-dc09-48bb-8363-5573c2f9aa81)


### **🔗 4-2. JDBC 드라이버 다운로드 및 설정**

- **MySQL Connector/J 다운로드**
    - [**MySQL Connector/J 다운로드 링크**](https://downloads.mysql.com/archives/c-j/)
    - 버전: **8.2.0**
    - 파일: Platform Independent (ZIP 파일) 다운로드
- **압축 해제 및 이동**
    1. 다운로드한 ZIP 파일 압축 해제
    2. 압축 해제된 폴더를 **ELK 설치 폴더의 하위 디렉토리**로 이동
 
        ![image3](https://github.com/user-attachments/assets/0ef030bd-cb1a-4f55-b1a7-94bc53af010f)
        
        예: `C:\logstash\jdbc` 
        
    - **참고**
        
        ![image4](https://github.com/user-attachments/assets/ea5e9c7e-ea9c-41b4-a84d-fb32422829c1)

        `mysql-connector-j-8.2.0.jar`의 경로를 JDBC 설정 시 사용

### **⚙️ 4-3. Logstash 설정 파일 (conf) 작성**

```
input {
  elasticsearch {
        hosts => ["http://localhost:9200"]  # Elasticsearch 호스트
        index => "stock"         # Elasticsearch 인덱스 이름
        query => '{
          "size": 1,
          "query": {
            "match_all": {}
          },
          "sort": [
            {
              "STCK_CNTG_HOUR": {
                "order": "desc"
              }
            }
          ]
        }'
        schedule => "*/10 * * * *"         # 매 10분마다 실행
    }
  # stdin{}
}

filter {
    ruby {
        code => '
            cntg_hour = event.get("STCK_CNTG_HOUR")
            if cntg_hour
                # ISO8601 형식을 MySQL DATETIME 형식으로 변환
                formatted_time = Time.parse(cntg_hour).strftime("%Y-%m-%d %H:%M:%S")
                event.set("STCK_CNTG_HOUR", formatted_time)
            end
        '
    }
}

output {
  # 콘솔창에 어떤 데이터들로 필터링 되었는지 확인
  stdout {
    codec => rubydebug
  }
  
  jdbc {
        driver_jar_path => "C:\\02.devEnv\\ELK\\mysql-connector-j-8.2.0\\mysql-connector-j-8.2.0.jar"  # MySQL JDBC 드라이버 경로
        driver_class => "com.mysql.cj.jdbc.Driver"
        connection_string => "jdbc:mysql://<ip>:<port>/stock?useSSL=false&allowPublicKeyRetrieval=true&user=<user id>&password=<user pw>"  # < >: 각자 환경의 데이터 삽입
        statement => [
            "INSERT INTO kr_stock_trade (mksc_shrn_iscd, stck_cntg_hour, stck_prpr, cntg_vol, acml_vol, stck_hgpr, stck_lwpr, now_time) VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            "%{MKSC_SHRN_ISCD}", "%{STCK_CNTG_HOUR}", "%{STCK_PRPR}", "%{CNTG_VOL}", "%{ACML_VOL}", "%{STCK_HGPR}", "%{STCK_LWPR}"
        ]
    }
}

```

- **구조**
    - `input` 섹션: 데이터 소스를 정의.
    - `filter` 섹션: 데이터 처리 및 변환 작업 정의.
    - `output` 섹션: 데이터베이스 연결 및 SQL 명령을 정의.


- **구현**
    1. **데이터 입력 (Input)**
        - elastic search의 데이터를 소스로 가져옴.
        - `schedule` 옵션을 통해 10분마다 실행
    2. **데이터 처리 (Filter)**
        - `ISO8601` 시간 형식을 MySQL의 `DATETIME` 형식으로 변환
    3. **데이터 출력 (Output)**
        - `output` 섹션에서 데이터베이스로 데이터를 내보내기 위해 `logstash-output-jdbc` 플러그인을 사용.
        - JDBC 드라이버를 통해 데이터베이스와 연결.
        - SQL 쿼리문을 실행하여 데이터를 테이블에 저장.

### 📊 4-참고. 구성 요소 간 비교 (플러그인 vs. 드라이버)

| **항목** | **logstash-output-jdbc 플러그인** | **JDBC 드라이버** |
| --- | --- | --- |
| **역할** | Logstash에서 데이터를 DB로 내보내는 기능 제공 | Logstash와 DB 간의 연결을 지원하는 통신 드라이버 |
| **사용 목적** | Logstash 파이프라인에서 SQL 쿼리 실행 | DB와 Logstash 간 데이터 송수신을 가능하게 함 |
| **설치 방식** | Logstash 플러그인 설치 명령어 사용 | MySQL Connector/J 등의 외부 파일 다운로드 필요 |
| **의존성** | JDBC 드라이버 설치가 필수 | 독립적으로 사용 가능 |

---

## 시연

--- 

## Troubleshooting
### Logstash 인스턴스 2개 실행 중 문제
방법1. Logstash 인스턴스를 2개 생성하기 위해 폴더 구조를 나누고 실제 실행도 나누어서 하는 방법
방법2. Logstash 실행시 파싱할 conf 파일 내에서 2가지 pipeline을 구성하여 1개의 인스턴스에서 실행하는 방법

### STCK_CNTG_HOUR값 mysql 이관 중 타입 오류

DATETIME 포멧에 지원하지 않는 표현식으로 인한 예외 발생
-> varchar(50)으로 적용시 문제 해결 가능 but 타입적인 문제는 없으나, 추후 Mysql에서 날짜 연산 시에 다시 파싱을 해야 연산이 가능한 문제가 예상되어 다음과 같이 Logstash conf 파일 내에서 filter 적용을 통해 ISO8601 형식을 DATETIME 형식으로 변환 후 insertion할 수 있었다.

``` ruby
filter {
    ruby {
        code => '
            cntg_hour = event.get("STCK_CNTG_HOUR")
            if cntg_hour
                # ISO8601 형식을 MySQL DATETIME 형식으로 변환
                formatted_time = Time.parse(cntg_hour).strftime("%Y-%m-%d %H:%M:%S")
                event.set("STCK_CNTG_HOUR", formatted_time)
            end
        '
    }
} 
```

### 지정된 시간마다 지정한 갯수의 row가 아닌 전체 row를 추가하는 문제

---

## 회고
