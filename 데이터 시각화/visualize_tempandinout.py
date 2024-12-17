# 필요한 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # Windows 기준
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터 파일 경로 설정
data_path = 'C:/Users/kym/Desktop/BD/project_v0.2/data/Data_ver.1.2_mapping.csv'

# 데이터 불러오기
df = pd.read_csv(data_path)

# 컬럼 이름 정리 (공백 제거)
df.columns = df.columns.str.strip()

# 데이터 전처리
df['확진자'] = df['확진자'].str.replace(',', '').astype(int)  # 확진자 수를 숫자로 변환
df = df[df['확진자'] < 2.5 * 10**6]  # 극단값 제거

# 기온과 습도에 따른 평균 확진자 수 계산
df['평균 기온 구간'] = pd.cut(df['평균 기온'], bins=10)  # 평균 기온을 10개 구간으로 나눔
df['평균 습도 구간'] = pd.cut(df['평균 습도'], bins=10)  # 평균 습도를 10개 구간으로 나눔

# 기온별 평균 확진자 계산
temp_group = df.groupby('평균 기온 구간')['확진자'].mean().reset_index()
temp_group['구간 중앙값'] = temp_group['평균 기온 구간'].apply(lambda x: x.mid)

# 습도별 평균 확진자 계산
humidity_group = df.groupby('평균 습도 구간')['확진자'].mean().reset_index()
humidity_group['구간 중앙값'] = humidity_group['평균 습도 구간'].apply(lambda x: x.mid)

# 1. 평균 기온/습도와 확진자 수 관계 분석 (로그 스케일)
plt.figure(figsize=(12, 6))

# 산점도 (평균 기온 vs 확진자 수, 로그 스케일)
plt.subplot(1, 2, 1)
sns.scatterplot(x=df['평균 기온'], y=df['확진자'], label='산점도', alpha=0.6)
plt.plot(temp_group['구간 중앙값'], temp_group['확진자'], color='blue', marker='o', label='평균 기온별 평균 확진자 수')
plt.yscale('log')  # Y축 로그 스케일 적용
plt.title('평균 기온과 확진자 수의 관계')
plt.xlabel('평균 기온')
plt.ylabel('확진자 수')
plt.legend()

# 산점도 (평균 습도 vs 확진자 수, 로그 스케일)
plt.subplot(1, 2, 2)
sns.scatterplot(x=df['평균 습도'], y=df['확진자'], label='산점도', alpha=0.6)
plt.plot(humidity_group['구간 중앙값'], humidity_group['확진자'], color='green', marker='o', label='평균 습도별 평균 확진자 수')
plt.yscale('log')  # Y축 로그 스케일 적용
plt.title('평균 습도와 확진자 수의 관계')
plt.xlabel('평균 습도')
plt.ylabel('확진자 수')
plt.legend()

plt.tight_layout()
plt.show()
