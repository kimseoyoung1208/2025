# app.py
import streamlit as st
from datetime import datetime
import json

# -------------------- 기본 설정 --------------------
st.set_page_config(page_title="MBTI Career Wizard", page_icon="🪄", layout="wide")

CSS = """
<style>
.huge{
  font-size:clamp(32px,6vw,68px);
  font-weight:900;
  background:linear-gradient(90deg,#0ea5e9,#a855f7,#f59e0b);
  -webkit-background-clip:text;background-clip:text;color:transparent;
  animation:glow 8s ease-in-out infinite;letter-spacing:.5px
}
@keyframes glow{0%{filter:drop-shadow(0 0 0 #fff0)}50%{filter:drop-shadow(0 0 12px #fff4)}100%{filter:drop-shadow(0 0 0 #fff0)}}
.card{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
  border-radius:18px;padding:16px 18px;box-shadow:0 10px 26px rgba(0,0,0,.25)}
.pill{display:inline-flex;gap:8px;align-items:center;padding:6px 12px;border-radius:999px;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);margin:6px 6px 0 0}
.small{font-size:13px;opacity:.8}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

ALL = ["INTJ","INTP","ENTJ","ENTP","INFJ","INFP","ENFJ","ENFP",
       "ISTJ","ISFJ","ESTJ","ESFJ","ISTP","ISFP","ESTP","ESFP"]

# -------------------- 규칙 기반 추천(짧은 데이터) --------------------
def clusters_and_strengths(mbti: str):
    N, S = ("N" in mbti), ("S" in mbti)
    T, F = ("T" in mbti), ("F" in mbti)
    J, P = ("J" in mbti), ("P" in mbti)
    E, I = ("E" in mbti), ("I" in mbti)

    if N and T:
        clusters = ["데이터·AI 🤖", "R&D 🔬", "전략 기획 📊"]
        strengths = ["논리적 문제해결 🧠", "시스템 설계 🏗️", "장기적 비전 🗺️"]
    elif N and F:
        clusters = ["교육·브랜드 📚🏷️", "콘텐츠 ✍️", "사회 영향 🌍"]
        strengths = ["공감력 🫶", "스토리텔링 📖", "가치 중심 🎯"]
    elif S and T:
        clusters = ["운영·품질 ⚙️", "재무·행정 🧾", "엔지니어링 🛠️"]
        strengths = ["정확성 ✅", "실행력 🏁", "위험관리 🛡️"]
    else:  # S and F
        clusters = ["보건·교육 🩺📚", "서비스 🤝", "디자인 🎨"]
        strengths = ["배려 💐", "실무 감각 👟", "협업 🤝"]

    jobs = []
    if N and T:
        jobs += ["데이터 사이언티스트 🧮", "AI 엔지니어 🤖", "제품 매니저 🎯", "전략 컨설턴트 📈"]
    if N and F:
        jobs += ["상담가 🕊️", "브랜드 스토리텔러 📖", "UX 라이터 🧷", "교육 기획자 📚"]
    if S and T:
        jobs += ["QA/품질관리 🔍", "프로세스 엔지니어 🔧", "프로젝트 매니저 🗂️", "보안 엔지니어 🔐"]
    if S and F:
        jobs += ["간호사 🩺", "교육 매니저 🧑‍🏫", "고객 성공 ⭐", "이벤트 플래너 🎪"]

    if J:  # 조직화 성향
        jobs += ["오퍼레이션 매니저 ⚙️", "PMO/프로그램 매니저 🗺️"]
    if P:  # 탐색 성향
        jobs += ["크리에이터 📹", "창업가/그로스 🚀"]
    if E:  # 대외
        jobs += ["세일즈 리드 🧲", "커뮤니티 매니저 🏘️"]
    if I:  # 심층
        jobs += ["리서치 엔지니어 🧪", "백엔드 개발자 💻"]

    # 중복 제거 & 상위 6개만
    seen = set()
    uniq = [j for j in jobs if not (j in seen or seen.add(j))]
    return clusters, strengths, uniq[:6]

def pill(text: str) -> str:
    return f"<span class='pill'>{text}</span>"

# -------------------- UI --------------------
col1, col2 = st.columns([0.7, 0.3])
with col1:
    st.markdown("<div class='huge'>MBTI Career Wizard 🪄💼✨</div>", unsafe_allow_html=True)
    st.write("MBTI를 고르면 성향과 어울리는 직업을 **이모지 뿜뿜**으로 추천해드려요! 🌈")
with col2:
    st.metric("오늘의 날짜", datetime.now().strftime("%Y-%m-%d"))

mbti = st.selectbox("당신의 MBTI를 선택하세요", ALL, index=ALL.index("ENFP"))
clusters, strengths, jobs = clusters_and_strengths(mbti)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### 🧑‍🎓 프로필 — **{mbti}**")
    st.markdown("**잘 맞는 분야**")
    st.markdown(" ".join(pill(x) for x in clusters), unsafe_allow_html=True)
    st.markdown("**강점**")
    st.markdown(" ".join(pill(x) for x in strengths), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌟 추천 직업 TOP 6")
    for j in jobs:
        st.markdown(f"- {j}")
    st.markdown("</div>", unsafe_allow_html=True)

colA, colB = st.columns([0.5,0.5])
with colA:
    if st.button("🎉 반짝이!"):
        st.balloons()
with colB:
    snapshot = {
        "mbti": mbti,
        "clusters": clusters,
        "strengths": strengths,
        "jobs_top6": jobs,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    st.download_button(
        "📥 결과 JSON 다운로드",
        data=json.dumps(snapshot, ensure_ascii=False, indent=2),
        file_name=f"career_{mbti}.json",
        mime="application/json",
    )

st.markdown(
    "<div class='small'>⚠️ 참고: MBTI는 자기이해를 돕는 도구일 뿐, 진로를 단정하지 않습니다. 경험과 학습 데이터로 나만의 경로를 만드세요! 🌱</div>",
    unsafe_allow_html=True,
)
