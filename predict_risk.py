import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from datetime import datetime
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load Data
data_ver = pd.ExcelFile("D:/CODE/bigdata/2024-12-10/Data_ver.1.3.xlsx")
gender_covid = pd.read_excel("D:/CODE/bigdata/2024-12-10/gender_covid.xlsx")
age_covid = pd.read_excel("D:/CODE/bigdata/2024-12-10/age_covid.xlsx")

# Process Data
data_ver_sheet1 = data_ver.parse('Sheet1')
data_ver_sheet1['개최기간'] = data_ver_sheet1['개최기간'].astype(str)
data_ver_sheet1['개최기간_변환'] = pd.to_datetime(data_ver_sheet1['개최기간'].apply(lambda x: f"20{x[:2]}-{x[2:]}-01"))

gender_covid['일자'] = pd.to_datetime(gender_covid['일자'])
age_covid['일자'] = pd.to_datetime(age_covid['일자'])

merged_data = pd.merge(data_ver_sheet1, gender_covid, left_on='개최기간_변환', right_on='일자', how='left')
merged_data = pd.merge(merged_data, age_covid, on='일자', how='left')

# Model Training
features = ['평균 기온', '평균 습도', '남성(명)', '여성(명)', '0-9세', '10-19세', '20-29세', '30-39세', '40-49세', '50-59세', '60-69세', '70-79세', '80세이상']
target = '해당 축제 달의 광역 지역의 확진자 수'

model_data = merged_data.dropna(subset=features + [target])
X = model_data[features]
y = np.where(model_data[target] > model_data[target].median(), 1, 0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Updated prediction function to use monthly data
# Updated prediction function for monthly data input
def predict_risk_monthly_input(age, gender, month_str):
    try:
        input_date = datetime.strptime(month_str, '%Y%m')
        input_month = input_date.strftime('%Y-%m')
    except ValueError:
        return "Invalid month format. Use YYYYMM."

    # 1. 기온과 습도 처리
    same_month = merged_data['일자'].dt.month == input_date.month
    avg_temp = merged_data.loc[same_month, '평균 기온'].mean()
    avg_humidity = merged_data.loc[same_month, '평균 습도'].mean()

    # 2. 코로나 확진자 데이터 추세 계산
    merged_data['month_num'] = (merged_data['일자'].dt.year * 12 + merged_data['일자'].dt.month)
    target_month_num = input_date.year * 12 + input_date.month

    X = merged_data['month_num'].values.reshape(-1, 1)
    poly = PolynomialFeatures(degree=1)
    X_poly = poly.fit_transform(X)

    # 성별에 따른 확진자 수 예측
    if gender == 1:  # 남성
        gender_model = LinearRegression()
        gender_model.fit(X_poly, merged_data['남성(명)'])
        predicted_gender_cases = gender_model.predict(poly.transform([[target_month_num]]))[0]
    else:  # 여성
        gender_model = LinearRegression()
        gender_model.fit(X_poly, merged_data['여성(명)'])
        predicted_gender_cases = gender_model.predict(poly.transform([[target_month_num]]))[0]

    # 나이 그룹 찾기
    age_group_cols = ['0-9세', '10-19세', '20-29세', '30-39세', 
                      '40-49세', '50-59세', '60-69세', '70-79세', '80세이상']
    age_groups = [range(0, 10), range(10, 20), range(20, 30), range(30, 40), 
                  range(40, 50), range(50, 60), range(60, 70), range(70, 80), range(80, 150)]
    
    user_age_group = next((col for col, rng in zip(age_group_cols, age_groups) if age in rng), None)
    
    # 해당 연령대의 확진자 수 예측
    age_model = LinearRegression()
    age_model.fit(X_poly, merged_data[user_age_group])
    predicted_age_cases = age_model.predict(poly.transform([[target_month_num]]))[0]

    # 입력 데이터 준비 (사용자의 성별과 연령대만 고려)
    input_data = [
        avg_temp,
        avg_humidity,
        predicted_gender_cases if gender == 1 else 0,  # 남성인 경우
        predicted_gender_cases if gender == 0 else 0,  # 여성인 경우
        predicted_age_cases if user_age_group == '0-9세' else 0,
        predicted_age_cases if user_age_group == '10-19세' else 0,
        predicted_age_cases if user_age_group == '20-29세' else 0,
        predicted_age_cases if user_age_group == '30-39세' else 0,
        predicted_age_cases if user_age_group == '40-49세' else 0,
        predicted_age_cases if user_age_group == '50-59세' else 0,
        predicted_age_cases if user_age_group == '60-69세' else 0,
        predicted_age_cases if user_age_group == '70-79세' else 0,
        predicted_age_cases if user_age_group == '80세이상' else 0
    ]

    # 예측
    risk_probability = rf_model.predict_proba([input_data])[0]
    high_risk_prob = risk_probability[1] * 100
    risk_label = "High Risk" if high_risk_prob > 50 else "Low Risk"
    
    return {
        "Predicted Risk": risk_label,
        "Risk Probability": high_risk_prob,
        "Used Values": {
            "Age Group": user_age_group,
            "Gender": "Male" if gender == 1 else "Female",
            "Average Temperature": float(round(avg_temp, 2)),
            "Average Humidity": float(round(avg_humidity, 2)),
            "Predicted Cases for Age Group": int(predicted_age_cases),
            "Predicted Cases for Gender": int(predicted_gender_cases)
        }
    }

# 결과를 보기 좋게 출력하는 함수 추가
def print_prediction_results(results):
    print("\n예측 결과:")
    print(f"위험도: {results['Predicted Risk']}")
    print(f"고위험 확률: {results['Risk Probability']:.1f}%")
#    print("\n입력 정보:")
#    print(f"연령대: {results['Used Values']['Age Group']}")
#    print(f"성별: {results['Used Values']['Gender']}")
#    print("\n사용된 값들:")
#    print(f"평균 기온: {results['Used Values']['Average Temperature']}°C")
#    print(f"평균 습도: {results['Used Values']['Average Humidity']}%")
#    print(f"해당 연령대 예상 확진자: {results['Used Values']['Predicted Cases for Age Group']:,}명")
#    print(f"해당 성별 예상 확진자: {results['Used Values']['Predicted Cases for Gender']:,}명")

# 테스트
test_age = 40
test_gender = 1
test_month = "202008"
results = predict_risk_monthly_input(test_age, test_gender, test_month)
print_prediction_results(results)
