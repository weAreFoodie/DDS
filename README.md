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

사진

| name | version |
|:--:|:--:|
| FileBeat | 7.11.1 |
| Logstash | 7.11.1 |
| Elasticsearch | 7.11.1 |
| Kibana | 7.11.1 |
| Mysql | 7.11.1 | -> 수정 필요
| Ubuntu | 7.11.1 | -> 수정 필요

---

## 데이터 구조

---

## 시연

--- 

## Troubleshooting

### Logstash 인스턴스 2개 실행 중 문제

### STCK_CNTG_HOUR값 mysql 이관 중 타입 오류

DATETIME 포멧에 지원하지 않는 표현식으로 인한 예외 발생

---

## 회고
