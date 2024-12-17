# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Titanic 데이터 불러오기 (파일 경로 수정)
train_data = pd.read_csv('data/data/Data_ver.1.2_mapping.csv')

# 'Name', 'Ticket', 'Cabin'과 같은 불필요한 열 제거
train_data.drop(columns=['Name', 'Ticket', 'Cabin'], inplace=True)

# 결측값 처리
train_data['Age'].fillna(train_data['Age'].mean(), inplace=True)
train_data['Embarked'].fillna(train_data['Embarked'].mode()[0], inplace=True)

# 'Sex'와 'Embarked' 열을 숫자로 변환
label_encoder = LabelEncoder()
train_data['Sex'] = label_encoder.fit_transform(train_data['Sex'])
train_data['Embarked'] = label_encoder.fit_transform(train_data['Embarked'])

# 독립 변수(X)와 종속 변수(y) 분리
X = train_data.drop(columns=['Survived'])  # 'Survived'는 타겟 변수
y = train_data['Survived']

# 랜덤포레스트 모델 학습
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X, y)

# 특성 중요도 추출
importances = rf_model.feature_importances_

# 특성 이름과 중요도를 데이터프레임으로 정리
feature_importances = pd.DataFrame({
    'Feature': X.columns,
    'Importance': importances
}).sort_values(by='Importance', ascending=False)

# 특성 중요도 출력
print(feature_importances)