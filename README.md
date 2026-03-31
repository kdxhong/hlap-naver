# 🚀 네이버 쇼핑 트렌드 통합 인사이트 대시보드 (hlap-naver)

이 프로젝트는 네이버 데이터랩(Shopping Insights) 및 검색 API를 활용하여 특정 카테고리의 쇼핑 트렌드를 분석하고, 실시간 검색 결과를 통합하여 제공하는 인터랙티브 대시보드입니다.

---

## 🌐 즉시 체험하기 (Live Demo)

별도의 설치 없이 아래 링크를 통해 웹에서 바로 대시보드를 확인해 보실 수 있습니다.

- **배포 주소**: [https://hlap-naver-jdi94aahqtuagjeo44nyt5.streamlit.app/](https://hlap-naver-jdi94aahqtuagjeo44nyt5.streamlit.app/)

> [!TIP]
> 직접 본인의 API 키를 사용하여 로컬에서 더욱 자유롭게 분석하고 싶다면 아래 **실행 가이드**를 따라주세요!

---

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

## 🚀 실행 가이드 (Quick Start)

처음 시작하시는 분들을 위해 단계별로 상세히 안내해 드립니다.

### 1단계: 네이버 오픈 API 권한 획득 (사전 준비)

프로젝트 실행을 위해서는 네이버 개발자 센터에서 발급받은 API 키가 필요합니다.

1. [네이버 개발자 센터](https://developers.naver.com/apps/#/register)에 접속하여 로그인합니다.
2. **Application 등록**을 선택합니다.
3. **사용 API**에 다음 항목들을 추가합니다:
   - **데이터랩 (쇼핑인사이트)**
   - **데이터랩 (검색어트렌드)**
   - **검색 (쇼핑, 블로그, 뉴스, 카페)**
4. 등록 완료 후 **Client ID**와 **Client Secret**을 따로 메모해 둡니다.

---

### 2단계: 로컬 환경 구축 및 라이브러리 설치

> [!NOTE]
> 이 가이드는 **Windows 10/11** 및 **PowerShell** 환경을 기준으로 작성되었습니다.

```powershell
# 1. 가상환경 생성 (최초 1회만 수행)
# .venv 라는 이름의 가상 폴더를 생성하여 라이브러리를 격리 관리합니다.
python -m venv .venv

# 2. 가상환경 활성화
# 실행 위치의 경로에 (.venv) 표시가 나타나면 성공입니다.
.venv\Scripts\activate

# 3. 필수 라이브러리 설치
# requirements.txt에 명시된 모든 패키지를 한 번에 설치합니다.
pip install -r requirements.txt
```

---

### 3단계: API 키 설정 (`.env` 파일 작성)

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고(혹은 `.env.example`을 복제하여) 발급받은 키를 입력합니다.

> [!IMPORTANT]
> `.env` 파일은 자격 증명이 포함되므로 **절대 GitHub에 공개되지 않도록 주의**해 주세요. (이미 `.gitignore`에 포함되어 있습니다.)

```env
# .env 파일 예시 (따옴표 없이 입력해 주세요)
NAVER_CLIENT_ID=여러분의_Client_ID
NAVER_CLIENT_SECRET=여러분의_Client_Secret
```

---

### 4단계: 대시보드 실행

모든 설정이 완료되었습니다! 아래 명령어로 대시보드를 실행합니다.

```powershell
streamlit run app.py
```

실행 후 브라우저가 자동으로 열리며, 열리지 않을 경우 명령행에 표시된 `http://localhost:8501` 주소를 주소창에 직접 입력하여 접속해 주세요.

---

## 🛠️ 문제 해결 (Troubleshooting)

- **`streamlit` 명령어를 찾을 수 없나요?**: 가상환경이 활성화(`.venv\Scripts\activate`)되어 있는지 확인해 주세요.
- **API 호출 시 401 오류가 발생하나요?**: `.env` 파일에 API 키가 오타 없이 입력되었는지, `Client ID`와 `Secret`이 바뀌지 않았는지 체크해 주세요.
- **한글 폰트가 깨지나요?**: 대시보드 내 시각화(Plotly)는 시스템 기본 폰트를 사용합니다. 최신 브라우저와 Windows 환경에서는 기본적으로 정상 출력됩니다.

© 2026 hlap-naver Project Team. 🚀 도움이 필요하시면 이슈를 남겨주세요!
