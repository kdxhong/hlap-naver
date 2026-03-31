# [상세] 네이버 쇼핑인사이트 API (Datalab) 전수 레퍼런스

네이버 쇼핑인사이트 API는 쇼핑 분야별 검색 클릭 추이와 상세 통계(기기, 성별, 연령별 등)를 JSON 형식으로 제공합니다. 이 문서는 모든 엔드포인트와 구현에 필요한 데이터를 상세히 수록합니다.

---

## 1. 요청 공통 사양 (Common Specification)

- **인증**: 비로그인 방식 (ID/Secret 헤더 전송)
- **메서드**: `POST`
- **데이터 형식**: `JSON` (Content-Type: `application/json`)
- **일일 한도**: 1,000회

| 헤더 필드명 | 설명 |
| :--- | :--- |
| `X-Naver-Client-Id` | 발급받은 클라이언트 아이디 |
| `X-Naver-Client-Secret` | 발급받은 클라이언트 시크릿 |

---

## 2. 엔드포인트 목록 및 상세 사양

### 2.1. 분류별 트렌드 조회 (Main Service)
| 엔드포인트 | 상세 설명 |
| :--- | :--- |
| `.../datalab/shopping/categories` | 특정 분야(카테고리)의 기간별 클릭 추이 조회 |
| `.../datalab/shopping/category/device` | 특정 분야 내 기기별(PC/Mobile) 통계 조회 |
| `.../datalab/shopping/category/gender` | 특정 분야 내 성별(남/여) 통계 조회 |
| `.../datalab/shopping/category/age` | 특정 분야 내 연령별(5세 단위) 통계 조회 |

### 2.2. 키워드별 트렌드 조회 (Keyword Service)
| 엔드포인트 | 상세 설명 |
| :--- | :--- |
| `.../datalab/shopping/category/keywords` | 특정 분야 내 지정 키워드들의 클릭 추이 및 점유율 조회 |
| `.../datalab/shopping/category/keyword/device` | 특정 키워드 내 기기별(PC/Mobile) 통계 조회 |
| `.../datalab/shopping/category/keyword/gender` | 특정 키워드 내 성별(남/여) 통계 조회 |
| `.../datalab/shopping/category/keyword/age` | 특정 키워드 내 연령별(5세 단위) 통계 조회 |

---

## 3. 요청 바디(JSON) 구조 상세

모든 API 요청 시 다음 구조의 JSON 데이터를 전송해야 합니다.

```json
{
  "startDate": "2023-01-01",  // 시작 날짜 (YYYY-MM-DD)
  "endDate": "2023-01-31",    // 종료 날짜 (YYYY-MM-DD)
  "timeUnit": "month",        // 구간 단위 (date, week, month)
  "category": "50000000",     // 조사 대상 카테고리 ID (쇼핑인사이트 카테고리 기준)
  "keyword": [                // (선택) 키워드별 조회 시 사용
      {"name": "패션의류/정장", "param": ["정장"]}
  ],
  "device": "pc",             // (선택) 기기 필터링 (pc, mo)
  "gender": "f",              // (선택) 성별 필터링 (m, f)
  "ages": ["20", "30"]        // (선택) 연령군 필터링 (1~12번 코드 리스트)
}
```

---

## 4. 통합 구현 예제 (Python - CSV 저장)

본 코드는 API 응답을 받아 `data/` 폴더 내에 CSV 형식으로 자동 저장합니다.

```python
import os
import sys
import urllib.request
import json
import csv
from datetime import datetime

# 인증 정보 설정
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
url = "https://openapi.naver.com/v1/datalab/shopping/categories"

# 저장 경로 설정
os.makedirs("data", exist_ok=True)
output_file = "data/shopping_trend_results.csv"

# 요청 파라미터 (JSON)
body = {
    "startDate": "2025-03-31",
    "endDate": "2026-03-30",
    "timeUnit": "date",
    "category": [
        {"name": "패션의류", "param": ["50000000"]}
    ],
    "device": "",
    "gender": "",
    "ages": []
}

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
request.add_header("Content-Type", "application/json")

try:
    response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
    rescode = response.getcode()
    
    if rescode == 200:
        result = json.loads(response.read().decode('utf-8'))
        
        # CSV 파일 생성 및 데이터 쓰기
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            # 헤더 작성
            writer.writerow(['날짜', '카테고리명', '클릭비율(ratio)'])
            
            for res in result['results']:
                title = res['title']
                for entry in res['data']:
                    writer.writerow([entry['period'], title, entry['ratio']])
        
        print(f"성공: 데이터가 '{output_file}'에 저장되었습니다.")
    else:
        print(f"Error Code: {rescode}")
except Exception as e:
    print(f"에러 발생: {e}")
```

---

## 5. 결과 데이터 해석 팁
- `ratio`: 요청 기간 내에서 가장 클릭량이 높았던 시점을 **100**으로 기준 삼아 산출된 값입니다.
- **연령 코드**: `1`(0~12세), `2`(13~18세), `3`(19~24세), `4`(25~29세), `5`(30~34세), `6`(35~39세) 등을 의미합니다.
- 조회가 되지 않을 경우 해당 기간 내 데이터 모수가 부족한 것일 수 있으므로 기간을 넓게 설정해 보시기 바랍니다.
