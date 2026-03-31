import os
import sys
import urllib.request
import json
import csv
from datetime import datetime

# .env 파일 로드를 위한 라이브러리 (pip install python-dotenv 필요)
try:
    from dotenv import load_dotenv
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path)
    else:
        # 현재 디렉토리에 없을 경우 상위 디렉토리 등 탐색 (기본값)
        load_dotenv()
except ImportError:
    pass

# ==========================================
# [설정] 네이버 API 자격 증명 (.env 파일에서 읽어옴)
# ------------------------------------------
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
# ==========================================

# 분석 설정 (2025-03-31 ~ 2026-03-30)
START_DATE = "2025-03-31"
END_DATE = "2026-03-30"
URL = "https://openapi.naver.com/v1/datalab/shopping/categories"
DATA_DIR = "data"
OUTPUT_FILE = os.path.join(DATA_DIR, "shopping_trend_2025_2026.csv")

# 카테고리 설정 (패션의류: 50000000)
CATEGORIES = [
    {"name": "패션의류", "param": ["50000000"]}
]

def collect_data():
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not CLIENT_ID or not CLIENT_SECRET:
        print("⚠️ [에러] .env 파일에서 NAVER_CLIENT_ID 또는 NAVER_CLIENT_SECRET을 찾을 수 없습니다.")
        return

    # 요청 바디 구성
    body = {
        "startDate": START_DATE,
        "endDate": END_DATE,
        "timeUnit": "date",
        "category": CATEGORIES
    }

    request = urllib.request.Request(URL)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    request.add_header("Content-Type", "application/json")

    try:
        print(f"🔄 데이터 수집 중... (기간: {START_DATE} ~ {END_DATE})")
        response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
        rescode = response.getcode()
        
        if rescode == 200:
            result = json.loads(response.read().decode('utf-8'))
            save_to_csv(result)
        else:
            print(f"❌ API 호출 실패 (상태 코드: {rescode})")
            
    except Exception as e:
        print(f"❌ 에러 발생: {e}")

def save_to_csv(api_result):
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['날짜', '카테고리명', '클릭비율(ratio)'])
            
            total_rows = 0
            for res in api_result['results']:
                title = res['title']
                for entry in res['data']:
                    writer.writerow([entry['period'], title, entry['ratio']])
                    total_rows += 1
            
        print(f"✅ 수집 완료: '{OUTPUT_FILE}' (총 {total_rows}행 저장)")
        check_peaks(api_result)
        
    except Exception as e:
        print(f"❌ 파일 저장 실패: {e}")

def check_peaks(api_result):
    print("\n🔍 트렌드 피크 지점 (Ratio=100) 확인:")
    for res in api_result['results']:
        peaks = [d['period'] for d in res['data'] if d['ratio'] == 100]
        if peaks:
            print(f"- {res['title']}: {', '.join(peaks)}")
        else:
            print(f"- {res['title']}: 피크 지점 없음 (데이터 부족 추정)")

if __name__ == "__main__":
    collect_data()
