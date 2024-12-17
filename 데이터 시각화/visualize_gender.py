# 필요한 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기준
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터 파일 경로 설정
data_path = 'C:/Users/kym/Desktop/BD/project_v0.2/data/Data_ver.1.2_mapping.csv'
gender_data_path = 'C:/Users/kym/Desktop/BD/project_v0.2/data/gender_covid.csv'

# 데이터 불러오기
df = pd.read_csv(data_path)
gender_df = pd.read_csv(gender_data_path)

# 컬럼 이름 정리 (공백 제거)
df.columns = df.columns.str.strip()
gender_df.columns = gender_df.columns.str.strip()

# 데이터 전처리
df['개최기간'] = pd.to_datetime(df['개최기간'], format='%b-%y', errors='coerce')  # 날짜 변환
df['장소'] = df['장소'].astype(int)  # 실내/외를 숫자로 변환
df['확진자'] = df['확진자'].str.replace(',', '').astype(int)  # 확진자 수를 숫자로 변환
df = df.dropna()  # 결측치 제거

# Gender 데이터 전처리
gender_df['일자'] = pd.to_datetime(gender_df['일자'], format='%b-%y', errors='coerce')
gender_df = gender_df.dropna()

# 1. 평균 기온/습도와 확진자 수 관계 분석
plt.figure(figsize=(12, 6))

# 산점도 (평균 기온 vs 확진자 수)
plt.subplot(1, 2, 1)
sns.scatterplot(x=df['평균 기온'], y=df['확진자'])
plt.title('평균 기온과 확진자 수의 관계')
plt.xlabel('평균 기온')
plt.ylabel('확진자 수')

# 산점도 (평균 습도 vs 확진자 수)
plt.subplot(1, 2, 2)
sns.scatterplot(x=df['평균 습도'], y=df['확진자'])
plt.title('평균 습도와 확진자 수의 관계')
plt.xlabel('평균 습도')
plt.ylabel('확진자 수')

plt.tight_layout()
plt.show()

# 상관계수 계산
correlation_temp = df['평균 기온'].corr(df['확진자'])
correlation_humidity = df['평균 습도'].corr(df['확진자'])
print(f"평균 기온과 확진자 수 상관계수: {correlation_temp:.2f}")
print(f"평균 습도와 확진자 수 상관계수: {correlation_humidity:.2f}")

# 2. 장소(실내/외)에 따른 확진자 수 차이 분석
indoor_cases = df[df['장소'] == 0]['확진자']
outdoor_cases = df[df['장소'] == 1]['확진자']

# t-test 수행
t_stat, p_value = ttest_ind(indoor_cases, outdoor_cases, equal_var=False)
print(f"t-statistic: {t_stat:.2f}, p-value: {p_value:.4f}")

# 실내/실외 평균 비교
indoor_mean = indoor_cases.mean()
outdoor_mean = outdoor_cases.mean()
print(f"실내 평균 확진자 수: {indoor_mean:.2f}")
print(f"실외 평균 확진자 수: {outdoor_mean:.2f}")

# 실내/실외 확진자 수 박스플롯
plt.figure(figsize=(8, 6))
sns.boxplot(x=df['장소'], y=df['확진자'], palette='Set3')
plt.xticks([0, 1], ['실내', '실외'])
plt.title('장소(실내/외)에 따른 확진자 수 분포')
plt.xlabel('장소 (0: 실내, 1: 실외)')
plt.ylabel('확진자 수')
plt.show()

# 3. 성별 확진자 수 시각화
plt.figure(figsize=(12, 6))

# 성별 확진자 수 선 그래프
plt.plot(gender_df['일자'], gender_df['남성(명)'], marker='o', label='남성 확진자 수', color='blue')
plt.plot(gender_df['일자'], gender_df['여성(명)'], marker='o', label='여성 확진자 수', color='red')
plt.title("성별 확진자 수 추이")
plt.xlabel("일자")
plt.ylabel("확진자 수")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# 4. 전체 데이터 상관관계 분석 (확진자, 평균 기온, 평균 습도, 장소)
correlation_matrix = df[['평균 기온', '평균 습도', '확진자', '장소']].corr()

# 상관관계 히트맵
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('확진자, 평균 기온, 평균 습도, 실내/외 상관관계 히트맵')
plt.show()
