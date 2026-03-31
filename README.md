# 🚀 네이버 쇼핑 트렌드 통합 인사이트 대시보드 (hlap-naver)

이 프로젝트는 네이버 데이터랩(Shopping Insights) 및 검색 API를 활용하여 특정 카테고리의 쇼핑 트렌드를 분석하고, 실시간 검색 결과를 통합하여 제공하는 인터랙티브 대시보드입니다.

## 🌟 주요 기능

### 📉 1. 키워드 트렌드 비교 (Trend Analysis)
- 최대 5개의 키워드에 대해 지난 1년간의 트래픽 추이를 시각화합니다.
- **주요 시각화**: 일별 시계열 라인 차트, 월간 누적 클릭량 바 차트, 요일별 평균 클릭비율 히트맵 등
- **데이터 분석**: 키워드별 기초 통계(평균, 최대/최소, 표준편차) 및 전일 대비 증감율 비교

### 🔍 2. 심층 EDA (Deep Dive)
- 특정 키워드에 대한 정밀한 통계 분석을 수행합니다.
- **분석 도구**:
    - **박스플롯(Boxplot)**: 월별 클릭비율 변동폭 및 이상치 확인
    - **바이올린 플롯(Violin Plot)**: 요일별 트래픽 밀도 분포 분석
    - **이동평균선(MA7)**: 노이즈를 제거한 트렌드 추세 파악
    - **차분(Difference) 그래프**: 급격한 트래픽 변화 시점(Momentum) 포착

### 📄 3. 통합 검색 결과 (Integrated Search)
- 네이버 쇼핑, 블로그, 카페, 뉴스 API를 통해 실시간 데이터를 호출합니다.
- **인터페이스**: 페이징 처리된 목록 제공 및 원본 페이지 하이퍼링크 연동

---

## 🛠️ 기술 스택
- **언어**: Python 3.8+
- **프레임워크**: Streamlit
- **시각화**: Plotly (Interactive Charts)
- **데이터 처리**: Pandas
- **인증 관리**: python-dotenv

---

## 🚀 실행 가이드

### 1단계: 환경 설정 및 가상환경 구축

```bash
# 레파지토리 클론 (필요 시)
# git clone https://github.com/kdxhong/hlap-naver.git
# cd hlap-naver

# 가상환경 생성 및 활성화
python -m venv .venv
source .venv/bin/scripts/activate  # Windows: .venv\Scripts\activate

# 라이브러리 설치
pip install -r requirements.txt
```

### 2단계: 네이버 API 키 설정
`.env` 파일을 생성하고 네이버 개발자 센터에서 발급받은 API 키를 입력합니다.

```env
NAVER_CLIENT_ID=your_client_id_here
NAVER_CLIENT_SECRET=your_client_secret_here
```

### 3단계: 애플리케이션 실행

```bash
streamlit run app.py
```

---

## 📂 프로젝트 구조
- `app.py`: Streamlit 대시보드 메인 소스 코드
- `collect_shopping_trend.py`: 데이터 수집 전용 스크립트
- `eda_analysis.py`: 데이터 분석 및 시각화 로직
- `docs/`: 프로젝트 설계서 및 API 레퍼런스 가이드
- `report/`: 생성된 정기 분석 리포트 보관함
- `.gitignore`: Git 제외 파일 설정 (.env, .venv 포함)

---
© 2026 hlap-naver Project. All rights reserved.
