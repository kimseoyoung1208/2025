import streamlit as st
import pandas as pd
import altair as alt

st.title("🔬 체질량 · 기초대사량 분석기 ")

# 사용자 입력
st.header("📥 정보 입력")
height = st.number_input("키 (cm)", min_value=100, max_value=250, value=None, placeholder="cm 단위로 입력하세요")
weight = st.number_input("몸무게 (kg)", min_value=30, max_value=200, value=None, placeholder="kg 단위로 입력하세요")
age = st.number_input("나이", min_value=10, max_value=100, value=None, placeholder="나이를 입력하세요")
gender = st.radio("성별", ("남성", "여성"), index=None)

activity_level = st.selectbox(
    "활동 수준",
    ("거의 운동 안 함", "가벼운 활동(주 1~3일)", "보통 활동(주 3~5일)", "적극적 활동(주 6~7일)", "매우 활동적(운동선수 수준)"),
    index=None,
    placeholder="활동 수준을 선택하세요"
)

if height and weight and age and gender and activity_level:
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

    # BMI 상태 구분
    if bmi < 18.5:
        status = "저체중"
    elif bmi < 23:
        status = "정상"
    elif bmi < 25:
        status = "과체중"
    else:
        status = "비만"

    # 정상 체중 범위
    min_weight = 18.5 * (height / 100) ** 2
    max_weight = 22.9 * (height / 100) ** 2

    # 3대 영양소
    carbs = tdee * 0.5 / 4   # g
    protein = tdee * 0.2 / 4 # g
    fat = tdee * 0.3 / 9     # g

    # 출력
    st.header("📊 결과")
    st.write(f"👉 **체질량지수 (BMI)**: {bmi:.2f} ({status})")
    st.write("📌 WHO 기준: 저체중 < 18.5 / 정상 18.5 ~ 22.9 / 과체중 23 ~ 24.9 / 비만 ≥ 25")


    st.write(f"👉 **기초대사량 (BMR)**: {bmr:.0f} kcal/day")
    st.write(f"👉 **하루 권장 섭취 칼로리 (TDEE)**: {tdee:.0f} kcal/day")

    if weight < min_weight:
        st.write(f"✅ 정상 체중에 도달하려면 약 **{min_weight - weight:.1f} kg** 증량이 필요합니다.")
    elif weight > max_weight:
        st.write(f"✅ 정상 체중에 도달하려면 약 **{weight - max_weight:.1f} kg** 감량이 필요합니다.")
    else:
        st.write("✅ 현재 체중은 정상 범위에 있습니다!")

    st.subheader("🍽️ 하루 권장 영양소 섭취량")
    st.write(f"- 탄수화물: {carbs:.0f} g")
    st.write(f"- 단백질: {protein:.0f} g")
    st.write(f"- 지방: {fat:.0f} g")

    # Altair 그래프 (y축 제목 세로 표시)
    st.subheader("📈 영양소 비율 시각화")
    df = pd.DataFrame({
        "영양소": ["탄수화물", "단백질", "지방"],
        "섭취량(g)": [carbs, protein, fat]
    })

    chart = (
        alt.Chart(df)
        .mark_bar(color="skyblue")
        .encode(
            x=alt.X("영양소:N", axis=alt.Axis(labelAngle=0)),  
            y=alt.Y("섭취량(g):Q", axis=alt.Axis(titleAngle=0)),  
            tooltip=["영양소", "섭취량(g)"]
        )
    )
    st.altair_chart(chart, use_container_width=True)

else:
    st.info("👉 키, 몸무게, 나이, 성별, 활동 수준을 모두 입력하면 결과가 표시됩니다!")

