import streamlit as st

st.title("🔬 체질량 · 기초대사량 분석기")

# 사용자 입력
st.header("📥 정보 입력")
height = st.number_input("키 (cm)", min_value=100, max_value=250, value=170)
weight = st.number_input("몸무게 (kg)", min_value=30, max_value=200, value=60)
age = st.number_input("나이", min_value=10, max_value=100, value=20)
gender = st.radio("성별", ("남성", "여성"))

activity_level = st.selectbox(
    "활동 수준",
    ("거의 운동 안 함", "가벼운 활동(주 1~3일)", "보통 활동(주 3~5일)", "적극적 활동(주 6~7일)", "매우 활동적(운동선수 수준)")
)

# BMI 계산
bmi = weight / ((height / 100) ** 2)

# BMR (Mifflin-St Jeor 공식)
if gender == "남성":
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
else:
    bmr = 10 * weight + 6.25 * height - 5 * age - 161

# 활동 수준별 계수
activity_factors = {
    "거의 운동 안 함": 1.2,
    "가벼운 활동(주 1~3일)": 1.375,
    "보통 활동(주 3~5일)": 1.55,
    "적극적 활동(주 6~7일)": 1.725,
    "매우 활동적(운동선수 수준)": 1.9
}

tdee = bmr * activity_factors[activity_level]

# 출력
st.header("📊 결과")
st.write(f"👉 **BMI**: {bmi:.2f}")
if bmi < 18.5:
    st.write("체중 상태: 저체중")
elif bmi < 23:
    st.write("체중 상태: 정상")
elif bmi < 25:
    st.write("체중 상태: 과체중")
else:
    st.write("체중 상태: 비만")

st.write(f"👉 **기초대사량 (BMR)**: {bmr:.0f} kcal/day")
st.write(f"👉 **하루 권장 섭취 칼로리 (TDEE)**: {tdee:.0f} kcal/day")
