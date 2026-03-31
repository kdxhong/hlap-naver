# [상세] 네이버 비로그인 오픈 API 가이드

네이버 오픈 API는 접근 편의성에 따라 **비로그인 방식**과 **로그인 방식**으로 구분됩니다. 본 가이드는 비로그인 방식 API의 특징과 전체 서비스 목록을 상세히 제공합니다.

## 1. 비로그인 방식 오픈 API란?
`HTTP Request Header`에 애플리케이션 등록 시 발급받은 **클라이언트 아이디**와 **클라이언트 시크릿** 값만 전송하여 사용할 수 있는 API입니다. 네이버 아이디 로그인을 통한 별도의 접근 토큰(Access Token) 획득 과정이 생략되어 구현이 간편합니다.

### 특징
- **사용량 합산**: API 사용량은 클라이언트 아이디(애플리케이션)별로 합산됩니다.
- **보안**: 클라이언트 시크릿은 외부로 유출되지 않도록 서버사이드에서 안전하게 처리해야 합니다.

---

## 2. 권한 인증 헤더 (Common)
모든 비로그인 API 호출 시 필수적으로 포함해야 하는 HTTP 헤더 정보입니다.

| 헤더 필드명 | 설명 |
| :--- | :--- |
| `X-Naver-Client-Id` | 네이버 개발자 센터에서 발급받은 클라이언트 ID |
| `X-Naver-Client-Secret` | 네이버 개발자 센터에서 발급받은 클라이언트 시크릿 |

---

## 3. 서비스별 상세 목록 (URL & Method)


### 3.1. 검색 (Search API)

| 서비스 | 인계서(Endpoint) | 메서드 |
| :--- | :--- | :---: |
| 뉴스 조회 | `https://openapi.naver.com/v1/search/news` | GET |
| 백과사전 조회 | `https://openapi.naver.com/v1/search/encyc` | GET |
| 블로그 조회 | `https://openapi.naver.com/v1/search/blog` | GET |
| **쇼핑 조회** | `https://openapi.naver.com/v1/search/shop` | GET |
| 웹문서 조회 | `https://openapi.naver.com/v1/search/webkr` | GET |
| 이미지 조회 | `https://openapi.naver.com/v1/search/image` | GET |
| 전문정보 조회 | `https://openapi.naver.com/v1/search/doc` | GET |
| 지식iN 조회 | `https://openapi.naver.com/v1/search/kin` | GET |
| 책 조회 | `https://openapi.naver.com/v1/search/book` | GET |
| 카페글 조회 | `https://openapi.naver.com/v1/search/cafearticle` | GET |
| 성인 검색어 판별 | `https://openapi.naver.com/v1/search/adult` | GET |
| 오타 변환 | `https://openapi.naver.com/v1/search/errata` | GET |
| 지역 검색 | `https://openapi.naver.com/v1/search/local` | GET |


### 3.2. 데이터랩 (DataLab API)

| 서비스 | 인계서(Endpoint) | 메서드 |
| :--- | :--- | :---: |
| 통합검색어 트렌드 | `https://openapi.naver.com/v1/datalab/search` | POST |
| 쇼핑인사이트 카테고리 | `https://openapi.naver.com/v1/datalab/shopping/categories` | POST |
| 쇼핑인사이트 기기별 | `https://openapi.naver.com/v1/datalab/shopping/category/device` | POST |
| 쇼핑인사이트 성별 | `https://openapi.naver.com/v1/datalab/shopping/category/gender` | POST |
| 쇼핑인사이트 연령별 | `https://openapi.naver.com/v1/datalab/shopping/category/age` | POST |
| 쇼핑인사이트 키워드별 | `https://openapi.naver.com/v1/datalab/shopping/category/keywords` | POST |

### 3.3. 얼굴 인식 (Clova Face Recognition)
| 서비스 | 인계서(Endpoint) | 메서드 |
| :--- | :--- | :---: |
| 얼굴 인식 | `https://openapi.naver.com/v1/vision/face` | POST |
| 유명인 인식 | `https://openapi.naver.com/v1/vision/celebrity` | POST |

### 3.4. 캡차 (Captcha API)
| 서비스 | 인계서(Endpoint) | 메서드 |
| :--- | :--- | :---: |
| 이미지 캡차 키 발급 | `https://openapi.naver.com/v1/captcha/nkey` | GET |
| 이미지 캡차 이미지 | `https://openapi.naver.com/v1/captcha/ncaptcha.bin` | GET |
| 음성 캡차 키 발급 | `https://openapi.naver.com/v1/captcha/skey` | GET |
| 음성 캡차 오디오 | `https://openapi.naver.com/v1/captcha/scaptcha` | GET |


### 3.5. 기타 유틸리티

| 서비스 | 인계서(Endpoint) | 메서드 |
| :--- | :--- | :---: |
| 네이버 공유하기 | `http://share.naver.com/web/shareView` | GET |
| 네이버 오픈메인 | (플러그인 방식 기반 제공) | - |

---

## 4. API 호출 한도 및 주의사항
- **Quota**: 각 API 서비스마다 하루(00:00~23:59) 호출 가능한 횟수가 제한되어 있습니다.
- **제한 확인**: 네이버 개발자 센터의 [Application > 내 애플리케이션] 메뉴에서 개별 API의 실시간 호출 현황을 확인할 수 있습니다.
- **권한 설정**: 애플리케이션 등록 후 반드시 [API 설정] 탭에서 사용하고자 하는 API 서비스를 추가해야만 해당 API를 호출할 수 있습니다. (설정하지 않을 시 403 Forbidden 에러 발생)
- **HTTPS 권장**: 모든 API 통신은 보안을 위해 HTTPS 프로토콜 사용을 권장합니다.
