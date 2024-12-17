# 필요한 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import matplotlib.ticker as ticker

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기준
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터 파일 경로 설정
data_path = 'C:/Users/kym/Desktop/BD/project_v0.2/data/Data_ver.1.2_mapping.csv'
age_data_path = 'C:/Users/kym/Desktop/BD/project_v0.2/data/age_covid.csv'

# 데이터 불러오기
df = pd.read_csv(data_path)
age_df = pd.read_csv(age_data_path)

# 컬럼 이름 정리 (공백 제거)
df.columns = df.columns.str.strip()
age_df.columns = age_df.columns.str.strip()

# 데이터 전처리
df['확진자'] = df['확진자'].str.replace(',', '').astype(int)  # 확진자 수를 숫자로 변환
df = df[df['확진자'] < 2.5 * 10**6]  # 극단값 제거

# 연월 컬럼 변환 (age_df)
age_df['연월'] = pd.to_datetime(age_df['연월'], format='%b-%y', errors='coerce')
age_df = age_df.melt(id_vars=['연월'], var_name='나이대', value_name='확진자수')  # Wide to long format
age_df = age_df.dropna()  # 결측치 제거

# 확진자 수가 0일 경우 1로 대체 (로그 스케일 적용 가능하도록)
age_df['확진자수'] = age_df['확진자수'].replace(0, 1)

# 나이대별 월간 확진자 추이 시각화 (로그 스케일 적용)
plt.figure(figsize=(16, 10))
sns.lineplot(data=age_df, x='연월', y='확진자수', hue='나이대', marker='o', linewidth=2.0, palette='tab10')

plt.yscale('log')  # 로그 스케일 적용
plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())  # 로그 스케일 숫자 표시
plt.gca().yaxis.set_minor_formatter(ticker.NullFormatter())  # 로그 스케일 소수점 표시 제거

# 그래프 제목과 레이블 설정
plt.title('나이대별 월간 확진자 수 추이', fontsize=16)
plt.xlabel('연월', fontsize=14)
plt.ylabel('확진자 수', fontsize=14)
plt.xticks(rotation=45)  # X축 레이블 회전
plt.grid(axis='y', linestyle='--', alpha=0.6)

# 범례 위치와 스타일 조정
plt.legend(title='나이대', loc='upper left', bbox_to_anchor=(1, 1), fontsize=12, title_fontsize=14)

plt.tight_layout()
plt.show()

# 나이대를 그룹화하여 서브플롯으로 표시
age_groups = {
    '젊은 층': ['0-9세', '10-19세', '20-29세'],
    '중년 층': ['30-39세', '40-49세', '50-59세'],
    '노년 층': ['60-69세', '70-79세', '80세이상']
}

# 서브플롯 설정
fig, axes = plt.subplots(3, 1, figsize=(14, 18), sharex=True)

for i, (group, categories) in enumerate(age_groups.items()):
    group_data = age_df[age_df['나이대'].isin(categories)]
    sns.lineplot(data=group_data, x='연월', y='확진자수', hue='나이대', marker='o', ax=axes[i], palette='tab10')
    axes[i].set_title(f'{group} 확진자 추이', fontsize=14)
    axes[i].set_xlabel('연월', fontsize=12)
    axes[i].set_ylabel('확진자 수', fontsize=12)
    axes[i].set_yscale('log')  # 로그 스케일
    axes[i].grid(axis='y', linestyle='--', alpha=0.6)
    axes[i].legend(title='나이대', loc='upper left', fontsize=10)

plt.tight_layout()
plt.show()
