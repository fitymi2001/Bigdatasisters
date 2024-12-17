import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc

# 한글 폰트 설정 (Windows 기준)
font_path = "C:/Windows/Fonts/malgun.ttf"  # Malgun Gothic 폰트 경로
font = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font)

# 데이터를 불러오고 필요한 열만 선택
df_festival = pd.read_excel('data/Data_ver.1.2.xlsx', sheet_name='Sheet1')  # 파일 경로와 시트 이름을 조정하세요
df_festival_filtered = df_festival[['축제유형', '확진자']].dropna()

# 축제 유형별 확진자 합계 계산
festival_summary = df_festival_filtered.groupby('축제유형')['확진자'].sum()

# 확진자 비율 계산
festival_summary_ratio = (festival_summary / festival_summary.sum()) * 100

# 비율 기준으로 상위 40%에 해당하는 축제 유형 필터링
festival_summary_sorted = festival_summary_ratio.sort_values(ascending=False)
cumulative_sum = festival_summary_sorted.cumsum()
top_40_percent = festival_summary_sorted[cumulative_sum <= 99.1]

# 결과 출력
print(top_40_percent)

# 그래프 그리기
plt.figure(figsize=(10, 6))
top_40_percent.plot(kind='bar', color='skyblue')
plt.title('축제 유형별 확진자 비율')
plt.xlabel('축제 유형')
plt.ylabel('확진자 비율 (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
