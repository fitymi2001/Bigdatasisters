import pandas as pd

# 파일 경로 설정
festival_path = "Data_20_ver.1.0.xlsx"  # festival 엑셀 파일 경로
temp_hum_path = "temp_hum_20-23.csv"  # temp_hum_20-23 CSV 파일 경로

# 1. 'festival' 엑셀 파일 읽기
festival_df = pd.read_excel(festival_path)

# 2. 'temp_hum_20-23' CSV 파일 읽기
temp_hum_df = pd.read_csv(temp_hum_path, encoding="cp949")  # 인코딩은 상황에 맞게 수정

# 3. 반복문을 통해 조건 수행
for idx in range(0, 10):  # 2행부터 11행까지 반복
    value_in_col4 = festival_df.iloc[idx, 4]  # 5열 값 (1~12의 정수)
    
    # 5열 값에 따라 필터링할 날짜를 생성
    if 2001 <= value_in_col4 <= 2012:  # 값이 2001~2012 사이의 정수인지 확인
        year = str(value_in_col4)[:2]
        month = str(value_in_col4)[2:4]  # 월을 두 자리 숫자로 변환 (예: 1 -> '01')
        target_date = f"20{year}-{month}-01"  # 해당 월의 첫 번째 날짜 생성
        
        # 'temp_hum_20-23'에서 1열 값이 col0_value와 같고, 2열 값이 target_date인 행 필터링
        col0_value = festival_df.iloc[idx, 0]  # 0열 값(string type)
        filtered_rows = temp_hum_df[
            (temp_hum_df.iloc[:, 1] == col0_value) &  # 1열 값이 일치
            (temp_hum_df.iloc[:, 2] == target_date)  # 2열 값이 target_date
        ]
        
        if not filtered_rows.empty:  # 조건을 만족하는 행이 있을 경우
            col3_value = filtered_rows.iloc[0, 3]  # 3열 값
            col8_value = filtered_rows.iloc[0, 8]  # 8열 값
            
            # 'festival' 파일의 9열과 10열에 값 쓰기
            festival_df.iloc[idx, 8] = col3_value  # 9열
            festival_df.iloc[idx, 9] = col8_value  # 10열

# 4. 수정된 데이터를 저장
output_path = "Data_20_ver.1.1.xlsx"  # 결과 저장 경로
festival_df.to_excel(output_path, index=False)

print(f"작업이 완료되었습니다. 수정된 데이터는 '{output_path}'에 저장되었습니다.")
