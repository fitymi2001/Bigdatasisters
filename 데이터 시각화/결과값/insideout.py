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

# 실내와 실외의 확진자 수 비율 계산
indoor_cases = df[df['장소'] == 0]['확진자'].sum()  # 실내 확진자 총합
outdoor_cases = df[df['장소'] == 1]['확진자'].sum()  # 실외 확진자 총합
total_cases = indoor_cases + outdoor_cases

indoor_ratio = (indoor_cases / total_cases) * 100  # 실내 비율
outdoor_ratio = (outdoor_cases / total_cases) * 100  # 실외 비율

# 박스플롯: 장소(실내/실외)에 따른 확진자 수 분포
plt.figure(figsize=(10, 6))
sns.boxplot(x=df['장소'], y=df['확진자'], palette='Set3')
plt.yscale('log')  # Y축 로그 스케일 적용
plt.xticks([0, 1], ['실내', '실외'])
plt.title('장소(실내/외)에 따른 확진자 수 분포 (로그 스케일)')
plt.xlabel('장소 (0: 실내, 1: 실외)')
plt.ylabel('확진자 수 (로그 스케일)')
plt.show()

# 실내와 실외 확진자 비율 시각화 (파이 차트)
plt.figure(figsize=(8, 6))
labels = ['실내', '실외']
ratios = [indoor_ratio, outdoor_ratio]
colors = ['skyblue', 'lightgreen']

plt.pie(ratios, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
plt.title('실내와 실외 확진자 비율')
plt.show()

# 실내와 실외 확진자 비율 시각화 (막대 그래프)
plt.figure(figsize=(8, 6))
sns.barplot(x=['실내', '실외'], y=[indoor_ratio, outdoor_ratio], palette='Set2')
plt.title('실내와 실외 확진자 비율 (%)')
plt.ylabel('확진자 비율 (%)')
plt.xlabel('장소')
plt.show()
