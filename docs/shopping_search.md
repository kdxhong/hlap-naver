# [상세] 네이버 쇼핑 검색 API 구현 가이드

본 문서는 네이버 쇼핑 검색 API를 사용하여 상품 정보를 조회하고자 하는 개발자를 위한 기술 참조 문서입니다.

## 1. API 기본 정보

| 항목 | 상세 내용 |
| :--- | :--- |
| **개요** | 네이버 쇼핑의 검색 결과를 JSON 또는 XML 형식으로 반환 |
| **인증 방식** | 비로그인 방식 (Client ID, Client Secret 헤더 전송) |
| **HTTP 메서드** | `GET` |
| **쿼리 한도** | 하루 최대 25,000회 |

### 요청 URL
- **JSON**: `https://openapi.naver.com/v1/search/shop.json`
- **XML**: `https://openapi.naver.com/v1/search/shop.xml`

---

## 2. 요청 파라미터 상세

| 파라미터 | 타입 | 필수 | 기본값 | 설명 |
| :--- | :--- | :---: | :---: | :--- |
| `query` | String | **Y** | - | **검색어**. UTF-8로 인코딩되어야 함. |
| `display` | Integer | N | 10 | **한 번에 표시할 결과 개수**. (최소 1, 최대 100) |
| `start` | Integer | N | 1 | **검색 시작 위치**. (최솟값 1, 최댓값 1000) |
| `sort` | String | N | `sim` | **정렬 옵션**:<br>- `sim`: 유사성(기본값)<br>- `date`: 날짜순<br>- `asc`: 가격 오름차순<br>- `dsc`: 가격 내림차순 |
| `filter` | String | N | - | **필터 옵션**: `naverpay` 지정 시 네이버페이 연동 상품만 노출. |
| `exclude` | String | N | - | **제외 옵션**: `{option}:{option}` 형태로 전달.<br>- `used`: 중고 상품 제외<br>- `rental`: 렌탈 상품 제외<br>- `cbshop`: 해외직구 상품 제외 |

---

## 3. 응답 필드 정의

### 3.1 공통 필드 (Channel)
- `lastBuildDate`: 검색 결과 생성 시간
- `total`: 전체 검색 결과 개수
- `start`: 검색 시작 위치
- `display`: 출력된 결과 개수

### 3.2 개별 아이템 필드 (Items)
| 필드명 | 설명 |
| :--- | :--- |
| `title` | 상품 명칭 (`<b>` 태그로 검색어 강조 포함) |
| `link` | 상품 상세 정보 URL |
| `image` | 상품 썸네일 이미지 URL |
| `lprice` | 최저가 (숫자 형태 문자열) |
| `hprice` | 최고가 (없을 경우 0) |
| `mallName` | 판매 쇼핑몰 명칭 |
| `productId` | 네이버 쇼핑 고유 상품 ID |
| `productType` | **상품군 타입**:<br>- `1`: 일반 상품 (가격비교 X)<br>- `2`: 가격비교 상품 (가격비교 O) |
| `brand` | 브랜드 정보 |
| `maker` | 제조사 정보 |
| `category1~4` | 네이버 쇼핑 카테고리 (대/중/소/세분류) |

---

## 4. 구현 예제 (Python - CSV 저장)

본 코드는 검색 결과를 `data/` 폴더 내에 CSV 형식으로 저장하는 완전한 예제입니다.

```python
import os
import sys
import urllib.request
import json
import csv

# 발급받은 자격 증명을 입력하세요
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# 저장 경로 설정
os.makedirs("data", exist_ok=True)
output_file = "data/shopping_search_results.csv"

encText = urllib.parse.quote("아이폰 15")
url = f"https://openapi.naver.com/v1/search/shop.json?query={encText}&display=20&sort=sim"

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)

try:
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    
    if rescode == 200:
        data = json.loads(response.read().decode('utf-8'))
        
        # CSV 파일 생성 및 데이터 쓰기
        with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            # 헤더 작성
            writer.writerow(['상품명', '최저가', '쇼핑몰', '카테고리', '링크'])
            
            for item in data['items']:
                title = item['title'].replace('<b>', '').replace('</b>', '')
                category = f"{item['category1']} > {item['category2']}"
                writer.writerow([title, item['lprice'], item['mallName'], category, item['link']])
        
        print(f"성공: 데이터가 '{output_file}'에 저장되었습니다. (총 {len(data['items'])}건)")
    else:
        print(f"Error Code: {rescode}")
except Exception as e:
    print(f"에러 발생: {e}")
```

---

## 5. 주요 오류 코드

| 상태 코드 | 상세 설명 | 해결 방법 |
| :---: | :--- | :--- |
| **400** | Bad Request | 파라미터 오타 및 필수 파라미터 누락 확인 |
| **401** | Unauthorized | 클라이언트 ID/Secret 값의 유효성 확인 |
| **403** | Forbidden | 서비스 권한 미설정 (개발자 센터 Application 설정 확인) |
| **429** | Too Many Requests | 호출 한도(일 25,000회) 초과 |
| **500** | Internal Server Error | 네이버 시스템 내부 오류 (잠시 후 재시도) |
