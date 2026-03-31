import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# 1. 환경 설정 및 데이터 로드
DATA_PATH = 'data/shopping_trend_2025_2026.csv'
IMAGE_DIR = 'images'
REPORT_DIR = 'report'
os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# 데이터 로드 (UTF-8-SIG는 한글 지원을 위해 사용)
df = pd.read_csv(DATA_PATH, encoding='utf-8-sig')

# 날짜 데이터 변환 및 파생 변수 생성
df['날짜'] = pd.to_datetime(df['날짜'])
df['연도'] = df['날짜'].dt.year
df['월'] = df['날짜'].dt.month
df['요일'] = df['날짜'].dt.day_name()
df['요일_num'] = df['날짜'].dt.dayofweek # 0:월, 6:일

# 요일 정렬을 위한 순서 정의
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_kr = {'Monday': '월', 'Tuesday': '화', 'Wednesday': '수', 'Thursday': '목', 'Friday': '금', 'Saturday': '토', 'Sunday': '일'}
df['요일_한글'] = df['요일'].map(days_kr)
df['요일_한글'] = pd.Categorical(df['요일_한글'], categories=['월', '화', '수', '목', '금', '토', '일'], ordered=True)

# 2. 기본 확인 및 기술 통계 (로그 기록용)
print("--- [기본 정보] ---")
print(f"전체 행/열: {df.shape}")
print("\n--- [상위 5개 행] ---")
print(df.head())
print("\n--- [하위 5개 행] ---")
print(df.tail())
print("\n--- [결측치 확인] ---")
print(df.isnull().sum())
print("\n--- [중복 데이터 확인] ---")
print(df.duplicated().sum())

print("\n--- [기술 통계 - 수치형] ---")
print(df.describe())

print("\n--- [기술 통계 - 범주형] ---")
print(df.describe(include=['O', 'category']))

# 3. 데이터 시각화 및 분석

def save_fig(name):
    plt.savefig(os.path.join(IMAGE_DIR, f"{name}.png"), bbox_inches='tight', dpi=300)
    plt.close()

# 1) 일별 클릭비율 트렌드 (시계열)
plt.figure(figsize=(15, 6))
sns.lineplot(data=df, x='날짜', y='클릭비율(ratio)', color='royalblue')
plt.title('2025-2026 네이버 쇼핑 클릭비율 일별 트렌드', fontsize=15)
plt.grid(True, linestyle='--', alpha=0.6)
save_fig('01_daily_trend')

# 2) 클릭비율 분포 히스토그램
plt.figure(figsize=(10, 6))
sns.histplot(df['클릭비율(ratio)'], bins=30, kde=True, color='seagreen')
plt.title('클릭비율 데이터 분포 현황', fontsize=15)
save_fig('02_ratio_dist')

# 3) 요일별 평균 클릭비율 분석
plt.figure(figsize=(10, 6))
day_avg = df.groupby('요일_한글')['클릭비율(ratio)'].mean().reset_index()
sns.barplot(data=day_avg, x='요일_한글', y='클릭비율(ratio)', palette='viridis')
plt.title('요일별 평균 클릭비율 비교', fontsize=15)
save_fig('03_day_of_week_avg')

# 4) 월별 평균 클릭비율 분석
plt.figure(figsize=(12, 6))
month_avg = df.groupby('월')['클릭비율(ratio)'].mean().reset_index()
sns.barplot(data=month_avg, x='월', y='클릭비율(ratio)', palette='magma')
plt.title('월별 평균 클릭비율 (상대적 수치)', fontsize=15)
save_fig('04_monthly_avg')

# 5) 전체 클릭비율 이상치 확인 (Boxplot)
plt.figure(figsize=(8, 6))
sns.boxplot(y=df['클릭비율(ratio)'], color='salmon')
plt.title('클릭비율 데이터 이상치 및 사분위수 분석', fontsize=15)
save_fig('05_outlier_check')

# 6) 월별 클릭비율 상세 분포 (Boxplot)
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='월', y='클릭비율(ratio)', palette='Set3')
plt.title('월별 클릭비율 분포 변동성', fontsize=15)
save_fig('06_monthly_box')

# 7) 7일 이동평균 추세선 분석
df['MA7'] = df['클릭비율(ratio)'].rolling(window=7).mean()
plt.figure(figsize=(15, 6))
plt.plot(df['날짜'], df['클릭비율(ratio)'], alpha=0.3, label='원본 데이터', color='gray')
plt.plot(df['날짜'], df['MA7'], color='red', linewidth=2, label='7일 이동평균')
plt.title('7일 이동평균 기반 쇼핑 트렌드 흐름', fontsize=15)
plt.legend()
save_fig('07_rolling_avg')

# 8) 요일별 클릭비율 상세 분포 (Violin Plot)
plt.figure(figsize=(12, 6))
sns.violinplot(data=df, x='요일_한글', y='클릭비율(ratio)', palette='pastel')
plt.title('요일별 클릭비율 밀도 및 분포 (Violin Plot)', fontsize=15)
save_fig('08_day_violin')

# 9) 월별 및 요일별 마케팅 히트맵 분석 (Pivot Table 활용)
pivot_df = df.pivot_table(values='클릭비율(ratio)', index='요일_한글', columns='월', aggfunc='mean')
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_df, annot=True, fmt=".1f", cmap='YlGnBu')
plt.title('월/요일별 평균 클릭비율 히트맵', fontsize=15)
save_fig('09_heatmap_analysis')

# 10) 전일 대비 클릭비율 변화량 분석
df['변화량'] = df['클릭비율(ratio)'].diff()
plt.figure(figsize=(15, 6))
plt.bar(df['날짜'], df['변화량'], color=df['변화량'].apply(lambda x: 'red' if x > 0 else 'blue'))
plt.title('전일 대비 클릭비율 증감 추이', fontsize=15)
plt.axhline(0, color='black', linewidth=1)
save_fig('10_diff_analysis')

# 4. 리포트용 추가 통계 생성 (CSV/Pickle 저장 대신 직접 출력)
print("\n--- [월별 평균 및 표준편차] ---")
print(df.groupby('월')['클릭비율(ratio)'].agg(['mean', 'std', 'max', 'min']))

print("\n--- [요일별 평균 및 표준편차] ---")
print(df.groupby('요일_한글')['클릭비율(ratio)'].agg(['mean', 'std']))

print("\n--- [최종 확인 완료] ---")
