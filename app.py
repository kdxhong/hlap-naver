import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as plt_go
import os
import urllib.request
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv

# 1. 환경 설정 및 로드
load_dotenv()
CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")

# 한글 폰트 설정 (Plotly는 시스템 폰트를 따름, Streamlit에서는 자동 지원되는 경우가 많음)
st.set_page_config(page_title="네이버 쇼핑 트렌드 통합 대시보드", layout="wide")

# 2. API 호출 함수 정의
@st.cache_data(ttl=3600)
def get_datalab_trend(keywords, start_date, end_date):
    url = "https://openapi.naver.com/v1/datalab/shopping/categories"
    
    # 키워드 그룹 구성 (최대 5개)
    keyword_groups = [{"name": kw, "param": [kw]} for kw in keywords if kw]
    
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "category": [{"name": "패션의류", "param": ["50000000"]}] # 대분류 기본값
    }
    # 실제 구현 시 키워드 검색은 '쇼핑인사이트' API보다는 '통합검색어 트렌드' API가 키워드 기반임
    # 여기서는 작업지시서에 따라 키워드 비교를 위한 데이터랩 API를 사용하되, 간소화된 통합검색어 트렌드 API 적용
    url = "https://openapi.naver.com/v1/datalab/search"
    body = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "date",
        "keywordGroups": [{"groupName": kw, "keywords": [kw]} for kw in keywords]
    }

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)
    request.add_header("Content-Type", "application/json")

    try:
        response = urllib.request.urlopen(request, data=json.dumps(body).encode("utf-8"))
        if response.getcode() == 200:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except Exception as e:
        st.error(f"데이터랩 API 호출 에러: {e}")
    return None

@st.cache_data(ttl=1800)
def get_naver_search(query, search_type="shop", display=10, start=1):
    api_map = {
        "shop": "search/shop",
        "blog": "search/blog",
        "cafe": "search/cafearticle",
        "news": "search/news"
    }
    url = f"https://openapi.naver.com/v1/{api_map[search_type]}?query={urllib.parse.quote(query)}&display={display}&start={start}"
    
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", CLIENT_ID)
    request.add_header("X-Naver-Client-Secret", CLIENT_SECRET)

    try:
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        st.error(f"검색 API({search_type}) 호출 에러: {e}")
    return None

# 3. 사이드바 구성
st.sidebar.title("📊 검색 설정")
if not CLIENT_ID or not CLIENT_SECRET:
    st.sidebar.error("⚠️ API Key가 설정되지 않았습니다. .env 파일을 확인해 주세요.")

search_keywords = st.sidebar.text_input("키워드 비교 (쉼표로 구분, 최대 5개)", "패션, 운동복, 후드티").split(",")
search_keywords = [kw.strip() for kw in search_keywords][:5]

period_option = st.sidebar.selectbox("분석 기간", ["최근 1개월", "최근 3개월", "최근 1년"])
end_dt = datetime.now()
if period_option == "최근 1개월":
    start_dt = end_dt - timedelta(days=30)
elif period_option == "최근 3개월":
    start_dt = end_dt - timedelta(days=90)
else:
    start_dt = end_dt - timedelta(days=365)

# 4. 메인 대시보드
st.title("🚀 네이버 쇼핑 트렌드 통합 인사이트")
st.markdown(f"**분석 범위**: {start_dt.strftime('%Y-%m-%d')} ~ {end_dt.strftime('%Y-%m-%d')} | **키워드**: {', '.join(search_keywords)}")

tab1, tab2, tab3 = st.tabs(["📉 트렌드 비교", "🔍 심층 EDA", "📄 통합 검색 결과"])

with tab1:
    st.header("키워드별 트래픽 트렌드 비교")
    trend_data = get_datalab_trend(search_keywords, start_dt.strftime('%Y-%m-%d'), end_dt.strftime('%Y-%m-%d'))
    
    if trend_data:
        # 데이터 정규화
        rows = []
        for group in trend_data['results']:
            name = group['title']
            for entry in group['data']:
                rows.append({"날짜": entry['period'], "키워드": name, "비율": entry['ratio']})
        
        df_trend = pd.DataFrame(rows)
        df_trend['날짜'] = pd.to_datetime(df_trend['날짜'])

        col1, col2 = st.columns([2, 1])
        
        with col1:
            # 1. 시계열 라인 차트 (Plotly)
            fig1 = px.line(df_trend, x="날짜", y="비율", color="키워드", title="일별 검색 트렌드 비교 (Ratio)", template="plotly_white")
            st.plotly_chart(fig1, use_container_width=True)
            
            # 2. 요일별 클릭비율 히트맵 (Pivot)
            df_trend['요일'] = df_trend['날짜'].dt.day_name()
            df_trend['월'] = df_trend['날짜'].dt.month
            pivot_day = df_trend.pivot_table(index='요일', columns='키워드', values='비율', aggfunc='mean').reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            fig_heat = px.imshow(pivot_day, text_auto=True, color_continuous_scale='YlGnBu', title="요일별 키워드 평균 호응도 (Heatmap)")
            st.plotly_chart(fig_heat, use_container_width=True)

        with col2:
            # 3. 누적 바 차트
            df_sum = df_trend.groupby('키워드')['비율'].sum().reset_index()
            fig3 = px.pie(df_sum, values='비율', names='키워드', title="전체 트래픽 점유율", hole=.3)
            st.plotly_chart(fig3, use_container_width=True)
            
            # 4. 기초 통계 비교표
            st.subheader("키워드별 기술 통계 요약")
            df_stats = df_trend.groupby('키워드')['비율'].agg(['mean', 'max', 'min', 'std']).round(2)
            st.table(df_stats)
            
            # 5. 전일 대비 증감율 순위
            st.subheader("최신 트렌드 변동 순위")
            latest_dates = sorted(df_trend['날짜'].unique())[-2:]
            if len(latest_dates) == 2:
                df_latest = df_trend[df_trend['날짜'].isin(latest_dates)].pivot(index='날짜', columns='키워드', values='비율')
                change = ((df_latest.iloc[1] - df_latest.iloc[0]) / df_latest.iloc[0] * 100).round(2)
                st.dataframe(change.sort_values(ascending=False).rename("전일비 증감(%)"))

with tab2:
    st.header("심층 EDA 및 분석 제언")
    selected_kw = st.selectbox("분석 대상 키워드 선택", search_keywords)
    df_single = df_trend[df_trend['키워드'] == selected_kw].copy()
    
    if not df_single.empty:
        col_ed1, col_ed2 = st.columns(2)
        
        with col_ed1:
            # 6. 월별 박스플롯
            fig_box = px.box(df_single, x="월", y="비율", title=f"[{selected_kw}] 월별 클릭비율 데이터 변동폭", color="월")
            st.plotly_chart(fig_box, use_container_width=True)
            
            # 7. 7일 이동평균선
            df_single['MA7'] = df_single['비율'].rolling(window=7).mean()
            fig_ma = plt_go.Figure()
            fig_ma.add_trace(plt_go.Scatter(x=df_single['날짜'], y=df_single['비율'], mode='lines', name='원본', line=dict(color='lightgray')))
            fig_ma.add_trace(plt_go.Scatter(x=df_single['날짜'], y=df_single['MA7'], mode='lines', name='7일 이동평균', line=dict(color='red', width=2)))
            fig_ma.update_layout(title=f"[{selected_kw}] 일별 추세 및 이동평균", template="plotly_white")
            st.plotly_chart(fig_ma, use_container_width=True)
            
            # 8. 바이올린 플롯
            fig_violin = px.violin(df_single, y="비율", x="요일", box=True, points="all", title=f"[{selected_kw}] 요일별 밀도 분석")
            st.plotly_chart(fig_violin, use_container_width=True)

        with col_ed2:
            # 9. 차분(Difference) 그래프
            df_single['diff'] = df_single['비율'].diff()
            fig_diff = px.bar(df_single, x='날짜', y='diff', title=f"[{selected_kw}] 전일 대비 클릭 증감량", color='diff', color_continuous_scale='RdBu_r')
            st.plotly_chart(fig_diff, use_container_width=True)
            
            # 10. 주간 성과 테이블 (Pivot)
            st.subheader(f"[{selected_kw}] 주간/월간 상세 성과표")
            df_single['주차'] = df_single['날짜'].dt.isocalendar().week
            weekly_pivot = df_single.groupby(['월', '주차'])['비율'].mean().round(1).unstack().fillna('-')
            st.dataframe(weekly_pivot)
            
            # 5개 이상의 표 구현 (기술통계, 상위 피크, 요일별 패턴, 이상치 감지 요약 등)
            st.markdown("---")
            peak_days = df_single.nlargest(5, '비율')[['날짜', '비율', '요일']]
            st.write("🚩 **트렌드 피크 상위 5일**")
            st.table(peak_days)
            
            # 이상치 요약
            q1, q3 = df_single['비율'].quantile([0.25, 0.75])
            iqr = q3 - q1
            outliers = df_single[(df_single['비율'] < q1 - 1.5 * iqr) | (df_single['비율'] > q3 + 1.5 * iqr)]
            st.write(f"📊 **이상치 감지 요약**: 전체 {len(df_single)}일 중 {len(outliers)}일 감지됨")

with tab3:
    st.header(f"'{selected_kw}' 통합 검색 결과")
    
    # 페이징 설정
    items_per_page = 10
    total_display = 100
    page = st.number_input("결과 페이지", min_value=1, max_value=total_display // items_per_page, value=1)
    start_idx = (page - 1) * items_per_page + 1
    
    search_type = st.radio("매체 선택", ["쇼핑", "블로그", "카페", "뉴스"], horizontal=True)
    type_map = {"쇼핑": "shop", "블로그": "blog", "카페": "cafe", "뉴스": "news"}
    
    results = get_naver_search(selected_kw, search_type=type_map[search_type], display=items_per_page, start=start_idx)
    
    if results and 'items' in results:
        for item in results['items']:
            with st.container():
                col_img, col_txt = st.columns([1, 4])
                title = item.get('title', '').replace('<b>', '').replace('</b>', '')
                link = item.get('link', '#')
                desc = item.get('description', '').replace('<b>', '').replace('</b>', '')
                
                with col_txt:
                    st.markdown(f"**[{title}]({link})**")
                    st.write(desc)
                    if 'mallName' in item: # 쇼핑전용
                        st.caption(f"판매처: {item['mallName']} | 가격: {item.get('lprice', '정보 없음')}원")
                
                with col_img:
                    if 'image' in item:
                        st.image(item['image'], width=100)
                    else:
                        st.markdown("🖼️") # 이미지 없을 때 대용
                st.divider()
    else:
        st.info("검색 결과가 없습니다.")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Naver Trend Dashboard | 전문 분석가 역할")
