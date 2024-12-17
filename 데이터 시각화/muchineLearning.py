# 필요한 라이브러리 임포트
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# 범주형 데이터 인코딩
label_encoder = LabelEncoder()
if '장소' in merged_df.columns:
    merged_df['장소'] = label_encoder.fit_transform(merged_df['장소'].astype(str))

# 결측값 처리 (평균값 또는 최빈값 대체)
for col in merged_df.select_dtypes(include=['number']).columns:
    merged_df[col].fillna(merged_df[col].mean(), inplace=True)

# 분석을 위한 특성 및 타겟 설정
X = merged_df[['계(명)_age', '남성(명)', '여성(명)', '평균 기온', '평균 습도']]  # 예시 특성
y = (merged_df['계(명)_age'] > 5000).astype(int)  # 타겟 예시: 5000명 이상이면 1, 아니면 0

# 학습 데이터와 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습 및 평가
kfold = KFold(n_splits=5, shuffle=True, random_state=42)
model = LogisticRegression(max_iter=1000)
scores = cross_val_score(model, X_train, y_train, cv=kfold)

print(f'교차 검증 평균 정확도: {scores.mean() * 100:.2f}%')

# 최종 모델 학습
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
print(f'테스트 데이터 정확도: {test_accuracy * 100:.2f}%')
