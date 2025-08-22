import streamlit as st
import random
import plotly.express as px

st.title("🌱 멘델의 유전 시뮬레이터")

st.write("""
부모의 대립유전자를 입력하면, 교배 후 자손의 유전자형과 표현형 비율을 시뮬레이션합니다.
예시: **R (둥근), r (주름)**
""")

# 부모 유전자 입력
parent1 = st.text_input("부모 1 유전자 (예: Rr)", value="Rr")
parent2 = st.text_input("부모 2 유전자 (예: Rr)", value="Rr")

num_offspring = st.slider("자손 수 선택", 50, 500, 100)

if st.button("시뮬레이션 실행"):
    offspring = []

    for _ in range(num_offspring):
        allele1 = random.choice(parent1)
        allele2 = random.choice(parent2)
        genotype = "".join(sorted([allele1, allele2]))
        offspring.append(genotype)

    # 유전자형 카운트
    genotype_counts = {g: offspring.count(g) for g in set(offspring)}

    # 표현형 계산 (대문자 하나라도 있으면 우성 표현형)
    phenotype_counts = {"우성 형질": 0, "열성 형질": 0}
    for g in offspring:
        if g[0].isupper() or g[1].isupper():
            phenotype_counts["우성 형질"] += 1
        else:
            phenotype_counts["열성 형질"] += 1

    st.subheader("🧬 결과")
    st.write("유전자형 비율:", genotype_counts)
    st.write("표현형 비율:", phenotype_counts)

    # Plotly 그래프 (유전자형)
    fig1 = px.bar(x=list(genotype_counts.keys()), y=list(genotype_counts.values()),
                  labels={'x':'유전자형', 'y':'개수'}, title="유전자형 분포")
    st.plotly_chart(fig1)

    # Plotly 그래프 (표현형)
    fig2 = px.bar(x=list(phenotype_counts.keys()), y=list(phenotype_counts.values()),
                  labels={'x':'표현형', 'y':'개수'}, title="표현형 분포",
                  color=list(phenotype_counts.keys()))
    st.plotly_chart(fig2)
