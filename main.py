import streamlit as st
from datetime import datetime
from typing import List, Dict

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="✨ MBTI Career Wizard",
    page_icon="🪄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# CSS Magic ✨
# -----------------------------
CSS = """
<style>
:root{
  --bg1:#0ea5e9; /* sky-500 */
  --bg2:#a855f7; /* purple-500 */
  --bg3:#f59e0b; /* amber-500 */
  --card:#111827; /* slate-900 */
  --text:#f8fafc; /* slate-50 */
  --muted:#cbd5e1; /* slate-300 */
  --pill:#1f2937; /* slate-800 */
}

/* Gradient animated title */
.huge-gradient{
  font-size: clamp(32px, 6vw, 72px);
  font-weight: 900;
  line-height: 1.05;
  background: linear-gradient(90deg, var(--bg1), var(--bg2), var(--bg3));
  background-size: 300% 300%;
  -webkit-background-clip: text; background-clip: text;
  color: transparent;
  animation: shine 8s ease-in-out infinite;
}
@keyframes shine{ 0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}}

/* Glass cards */
.card{
  background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 18px;
  padding: 18px 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.25);
}
.card h3{ margin-top:0; color: var(--text); }

/* Emoji pills */
.pill{
  display:inline-flex; align-items:center; gap:8px;
  padding:8px 12px; border-radius:999px; font-weight:700;
  background: linear-gradient(90deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
  border: 1px solid rgba(255,255,255,0.12);
  margin:6px 6px 0 0; color: var(--text); font-size: 14px;
}
.small{ font-size:13px; color:var(--muted); }

/* Subtitle */
.subtitle{ font-size: clamp(16px, 2.2vw, 22px); color: var(--muted); margin-top:-8px; }

/* Footer note */
.note{ font-size:13px; color:var(--muted); }

/* Align Streamlit native widgets a bit nicer */
.block-container{ padding-top: 1.2rem; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------
# Data: MBTI → Career Clusters & Traits
# -----------------------------
MBTI_DB: Dict[str, Dict[str, List[str]]] = {
    "INTJ": {
        "title": "전략가 🧠🗺️",
        "clusters": ["데이터·AI", "연구·R&D", "엔지니어링", "기획·전략"],
        "jobs": [
            "데이터 사이언티스트 🧮", "AI 리서처 🤖", "제품 매니저 🧭",
            "시스템 아키텍트 🏗️", "전략 컨설턴트 📊", "연구원 🔬"
        ],
        "strengths": ["장기적 비전", "논리적 문제 해결", "독립적 몰입"],
        "growth": ["협업 피드백 수용", "완벽주의 균형", "가설 검증 주기 단축"]
    },
    "INTP": {
        "title": "사색가 🧩",
        "clusters": ["연구·R&D", "소프트웨어", "데이터·AI"],
        "jobs": ["리서치 엔지니어 🧪", "백엔드 개발자 💻", "알고리즘 엔지니어 🧠", "보안 연구원 🛡️"],
        "strengths": ["개념화·추상화", "체계 설계", "지적 호기심"],
        "growth": ["프로토타입 빠르게", "완성도 집착 줄이기", "커뮤니케이션 기록"]
    },
    "ENTJ": {
        "title": "감독관 🧭",
        "clusters": ["기획·전략", "비즈니스", "프로덕트"],
        "jobs": ["프로덕트 매니저 🎯", "전략 컨설턴트 📈", "사업개발(BD) 🤝", "오퍼레이션 매니저 ⚙️"],
        "strengths": ["조직화·리더십", "목표 지향", "의사결정"],
        "growth": ["팀 속도 조율", "경청·공감", "리스크 관리"]
    },
    "ENTP": {
        "title": "발명가 💡",
        "clusters": ["스타트업", "마케팅", "프로덕트"],
        "jobs": ["그로스 마케터 📣", "창업가 🚀", "UX 전략가 🧭", "신사업 기획자 🧪"],
        "strengths": ["아이디어 발상", "빠른 학습", "설득"],
        "growth": ["실행력 구조화", "우선순위 명확화", "지속성 강화"]
    },
    "INFJ": {
        "title": "옹호자 🕊️",
        "clusters": ["교육·연구", "사회 영향", "콘텐츠"],
        "jobs": ["교육 기획자 📚", "상담가 🫶", "에디터 ✍️", "브랜드 스토리텔러 📖"],
        "strengths": ["가치 중심", "깊은 통찰", "공감"],
        "growth": ["경계 설정", "데이터 기반 의사결정", "지속 가능한 에너지 관리"]
    },
    "INFP": {
        "title": "중재자 🦋",
        "clusters": ["콘텐츠", "디자인", "사회 영향"],
        "jobs": ["작가 ✒️", "일러스트레이터 🎨", "UX 라이터 🧷", "NGO 활동가 🌍"],
        "strengths": ["창의적 표현", "의미 추구", "개인화"],
        "growth": ["마감 관리", "피드백 루프 만들기", "측정 가능한 목표"]
    },
    "ENFJ": {
        "title": "선도자 🌟",
        "clusters": ["교육", "HR·조직개발", "브랜딩"],
        "jobs": ["HRD 기획자 🧩", "조직문화 매니저 🧑‍🤝‍🧑", "커뮤니티 매니저 🏘️", "홍보(PR) 📣"],
        "strengths": ["코칭", "협업 촉진", "커뮤니케이션"],
        "growth": ["데이터 리터러시", "경영 지표 이해", "경계 관리"]
    },
    "ENFP": {
        "title": "활동가 🎉",
        "clusters": ["마케팅", "콘텐츠", "스타트업"],
        "jobs": ["크리에이티브 마케터 🎈", "크리에이터 📹", "프로덕트 에반젤리스트 📢", "CX 기획자 💬"],
        "strengths": ["네트워킹", "아이디어 발산", "에너지"],
        "growth": ["지속성·루틴", "우선순위", "실행 추적"]
    },
    "ISTJ": {
        "title": "현실주의자 🧱",
        "clusters": ["공공·행정", "재무·회계", "품질·운영"],
        "jobs": ["회계사 🧾", "품질관리(QA) 🔍", "프로세스 엔지니어 🛠️", "공무원 🏛️"],
        "strengths": ["정확성", "책임감", "절차 충실"],
        "growth": ["유연성 확보", "변화관리", "사용자 관점"]
    },
    "ISFJ": {
        "title": "수호자 🛡️",
        "clusters": ["보건·의료", "교육", "운영"],
        "jobs": ["간호사 🩺", "임상 코디네이터 🧫", "학사 운영 📋", "고객 성공 🤝"],
        "strengths": ["헌신", "디테일", "배려"],
        "growth": ["경계 설정", "데이터 도구 학습", "영향도 기반 우선순위"]
    },
    "ESTJ": {
        "title": "경영자 🏁",
        "clusters": ["운영·물류", "프로젝트", "비즈니스"],
        "jobs": ["프로젝트 매니저 🗂️", "오퍼레이션 리드 ⚙️", "구매/소싱 🧾", "세일즈 매니저 🧲"],
        "strengths": ["실행력", "조직화", "책임감"],
        "growth": ["혁신 수용", "팀 감정선 관리", "위임"]
    },
    "ESFJ": {
        "title": "사교가 🤝",
        "clusters": ["교육·서비스", "HR", "브랜드"],
        "jobs": ["교육 매니저 🧑‍🏫", "리크루터 🧑‍💼", "브랜드 매니저 🏷️", "고객 성공 ⭐"],
        "strengths": ["협력", "서비스 마인드", "관계 형성"],
        "growth": ["데이터 근거 제시", "갈등 관리", "장기 전략 학습"]
    },
    "ISTP": {
        "title": "장인 🛠️",
        "clusters": ["엔지니어링", "보안", "현장"],
        "jobs": ["하드웨어 엔지니어 🔧", "소프트웨어 엔지니어 💻", "보안 엔지니어 🔐", "필드 엔지니어 🧰"],
        "strengths": ["문제 해결", "도구 활용", "냉정함"],
        "growth": ["문서화 습관", "커뮤니케이션", "장기 계획"]
    },
    "ISFP": {
        "title": "모험가 🏕️",
        "clusters": ["디자인", "콘텐츠", "라이프스타일"],
        "jobs": ["그래픽 디자이너 🎨", "포토/영상 크리에이터 📷", "공방 운영자 🧵", "푸드 스타일리스트 🍰"],
        "strengths": ["감각", "진정성", "현장 적응"],
        "growth": ["비즈니스 관점", "포트폴리오 운영", "협업 루프"]
    },
    "ESTP": {
        "title": "사업가 💼",
        "clusters": ["세일즈", "마케팅", "현장"],
        "jobs": ["세일즈 리드 🧲", "퍼포먼스 마케터 📈", "프로듀서 🎬", "이벤트 디렉터 🎪"],
        "strengths": ["행동력", "순발력", "협상"],
        "growth": ["지속 전략", "리스크 분산", "데이터 추적"]
    },
    "ESFP": {
        "title": "연예인 🌈",
        "clusters": ["엔터·미디어", "마케팅", "서비스"],
        "jobs": ["MC/호스트 🎤", "SNS 크리에이터 📱", "광고 AE 🧷", "이벤트 플래너 🎈"],
        "strengths": ["현장 에너지", "관계 확장", "즉흥성"],
        "growth": ["재무 관리", "브랜드 일관성", "장기 프로젝트"]
    },
    "INFJ": MBTI_DB.get("INFJ", {
        "title": "옹호자 🕊️",
        "clusters": ["교육·연구", "사회 영향", "콘텐츠"],
        "jobs": ["교육 기획자 📚", "상담가 🫶", "에디터 ✍️", "브랜드 스토리텔러 📖"],
        "strengths": ["가치 중심", "깊은 통찰", "공감"],
        "growth": ["경계 설정", "데이터 기반 의사결정", "지속 가능한 에너지 관리"]
    }),
    "INFJ2": {},  # placeholder to prevent dict merge issues in editors
    "ENFP2": {},  # placeholder
}

# Fill the remaining types not explicitly defined above
DEFAULTS = {
    "title": "탐험가 ✨",
    "clusters": ["탐구", "창의", "협업"],
    "jobs": ["프로젝트 리서처 🔎", "콘텐츠 메이커 🎥", "커뮤니티 빌더 🧑‍🤝‍🧑"],
    "strengths": ["호기심", "학습", "소통"],
    "growth": ["우선순위", "기록 습관", "데이터 감각"]
}

ALL_TYPES = [
    "INTJ","INTP","ENTJ","ENTP",
    "INFJ","INFP","ENFJ","ENFP",
    "ISTJ","ISFJ","ESTJ","ESFJ",
    "ISTP","ISFP","ESTP","ESFP"
]

for t in ALL_TYPES:
    if t not in MBTI_DB or not MBTI_DB.get(t):
        MBTI_DB[t] = DEFAULTS.copy()

# -----------------------------
# Interest & Style dictionaries
# -----------------------------
INTERESTS = {
    "Tech & Data 💾": ["데이터 사이언스", "소프트웨어", "AI/ML", "클라우드"],
    "Healthcare 🩺": ["의료", "바이오", "임상", "헬스케어 운영"],
    "Business & Finance 💹": ["전략", "회계/재무", "세일즈", "컨설팅"],
    "Art & Design 🎨": ["그래픽", "UX/UI", "영상", "브랜딩"],
    "Education & Research 📚": ["교육", "학습과학", "연구", "문헌 분석"],
    "Social Impact 🌍": ["비영리", "정책", "환경", "지역사회"],
    "Nature & Field 🌿": ["환경과학", "지리", "에너지", "현장"],
    "Media & Content 📺": ["저널리즘", "SNS", "광고", "스토리텔링"],
}

STYLE_KEYS = {
    "team": ("혼자 🧘", "함께 👯"),
    "structure": ("자유 🌈", "정돈 🗂️"),
    "people": ("아이디어 💡", "사람 👥"),
}

# -----------------------------
# Helpers
# -----------------------------

def pill(text: str) -> str:
    return f'<span class="pill">{text}</span>'


def pill_row(title: str, items: List[str]) -> None:
    st.markdown(f"<div class='small'>{title}</div>" + " ".join(pill(i) for i in items), unsafe_allow_html=True)


def score_jobs(mbti: str, picks: List[str], style: Dict[str, int]) -> List[Dict]:
    import random
    base = MBTI_DB[mbti]["jobs"]
    scored = []
    for j in base:
        s = 50
        # Interest alignment
        for g in picks:
            if ("데이터" in j or "AI" in j or "개발" in j) and "Tech & Data" in g:
                s += 15
            if ("간호" in j or "임상" in j) and "Healthcare" in g:
                s += 15
            if ("전략" in j or "세일즈" in j or "사업" in j) and "Business" in g:
                s += 12
            if ("디자" in j or "크리에" in j or "브랜드" in j) and "Art & Design" in g:
                s += 12
            if ("교육" in j or "에디터" in j) and "Education" in g:
                s += 12
            if ("NGO" in j or "상담" in j) and "Social Impact" in g:
                s += 10
        # Style nudges
        s += (style["team"] - 50) / 5  # team
        s += (style["structure"] - 50) / 8  # structure
        s += (style["people"] - 50) / 6  # people
        s += random.uniform(-3, 3)
        scored.append({"job": j, "score": round(s, 1)})
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored

# -----------------------------
# Header
# -----------------------------
left, right = st.columns([0.72, 0.28])
with left:
    st.markdown("<div class='huge-gradient'>MBTI Career Wizard 🪄💼✨</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>MBTI를 선택하면 당신의 성향에 맞춘 직업 아이디어를 ✨화려하게✨ 추천해드려요! </div>", unsafe_allow_html=True)
with right:
    st.metric("오늘의 날짜", datetime.now().strftime("%Y-%m-%d"), help="오늘도 성장하는 당신에게 💖")

st.write("")

# -----------------------------
# Sidebar — Controls
# -----------------------------
with st.sidebar:
    st.markdown("## 🎛️ 마법 설정")
    mbti = st.selectbox("당신의 MBTI를 선택하세요", ALL_TYPES, index=ALL_TYPES.index("ENFP"))

    st.markdown("### 🎯 관심 분야")
    user_interests = st.multiselect("관심 있는 분야를 골라주세요 (복수 선택)", list(INTERESTS.keys()), default=["Tech & Data 💾", "Media & Content 📺"])

    st.markdown("### 🎚️ 일하는 스타일")
    team = st.slider(f"{STYLE_KEYS['team'][0]} ↔ {STYLE_KEYS['team'][1]}", 0, 100, 60)
    structure = st.slider(f"{STYLE_KEYS['structure'][0]} ↔ {STYLE_KEYS['structure'][1]}", 0, 100, 55)
    people = st.slider(f"{STYLE_KEYS['people'][0]} ↔ {STYLE_KEYS['people'][1]}", 0, 100, 70)

    st.markdown("—" * 20)
    st.markdown("#### 📦 내보내기")
    export_btn = st.button("추천 결과에 🎉 반짝이 뿌리기 & 저장하기")

# -----------------------------
# Content — Profile & Recommendations
# -----------------------------
profile = MBTI_DB[mbti]

c1, c2 = st.columns([1,1])
with c1:
    st.markdown(f"""
    <div class='card'>
      <h3>🧑‍🎓 MBTI 프로필 — {mbti} · {profile['title']}</h3>
      <div class='small'>나와 잘 맞는 분야</div>
      {" ".join(pill(c) for c in profile['clusters'])}
      <div style='height:8px'></div>
      <div class='small'>강점</div>
      {" ".join(pill(s) for s in profile['strengths'])}
      <div style='height:8px'></div>
      <div class='small'>성장 포인트</div>
      {" ".join(pill(g) for g in profile['growth'])}
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3>🎨 나의 관심 태그</h3>", unsafe_allow_html=True)
    for g in user_interests:
        pill_row(g, INTERESTS[g])
    st.markdown("</div>", unsafe_allow_html=True)

# Compute recommendations
style_dict = {"team": team, "structure": structure, "people": people}
scored = score_jobs(mbti, user_interests, style_dict)

st.markdown("### 🌈 추천 직업 TOP 6")
rc1, rc2, rc3 = st.columns(3)
cols = [rc1, rc2, rc3]

for i, item in enumerate(scored[:6]):
    col = cols[i % 3]
    with col:
        st.markdown(f"""
        <div class='card'>
          <h3>{item['job']}</h3>
          <div class='small'>적합도 점수 ⭐ {item['score']}</div>
          <div style='height:8px'></div>
          <div>{pill('이 직무와 어울리는 이유 💡')} {pill('나의 스타일과 시너지 🔗')}</div>
          <div style='height:8px'></div>
          <div class='note'>힌트: 직무 공고를 살펴보고 요구 역량을 체크리스트로 만들어 보세요. 포트폴리오/프로젝트로 역량을 증명하면 좋아요! ✨</div>
        </div>
        """, unsafe_allow_html=True)

# Tips & Next steps
st.markdown("### 🛠️ 다음 단계 제안")
t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("""
    <div class='card'>
    <h3>📚 공부 루트</h3>
    <div class='small'>MOOC · 튜토리얼 · 커뮤니티</div>
    <div>• 기본기: 수학/논리/통계 기초 다지기 📐<br>
         • 튜토리얼: 100일 미니 프로젝트 달리기 🏃<br>
         • 커뮤니티: 관심 분야 오픈소스/스터디 합류 🤝</div>
    </div>
    """, unsafe_allow_html=True)
with t2:
    st.markdown("""
    <div class='card'>
    <h3>🧰 포트폴리오 아이디어</h3>
    <div>• 데이터: 개인 관심사 분석 대시보드 📊<br>
         • 디자인: 앱 리디자인 케이스 스터디 🎨<br>
         • 교육: 튜토리얼 글 3편 연재 ✍️</div>
    </div>
    """, unsafe_allow_html=True)
with t3:
    st.markdown("""
    <div class='card'>
    <h3>🗺️ 커리어 전략</h3>
    <div>• 롤모델 3명 벤치마킹 🔭<br>
         • 역량 매트릭스 작성 ✅<br>
         • 30-60-90일 학습 플랜 📅</div>
    </div>
    """, unsafe_allow_html=True)

# Celebration & Export
if export_btn:
    st.balloons()
    # Save snapshot text
    snapshot = {
        "mbti": mbti,
        "interests": user_interests,
        "style": style_dict,
        "top6": scored[:6],
        "timestamp": datetime.now().isoformat(timespec='seconds')
    }
    import json, io
    buf = io.BytesIO()
    buf.write(json.dumps(snapshot, ensure_ascii=False, indent=2).encode('utf-8'))
    st.download_button(
        label="📥 추천 결과 JSON 다운로드",
        data=buf.getvalue(),
        file_name=f"career_reco_{mbti}.json",
        mime="application/json",
        help="나중에 다시 불러오거나 공유해보세요!"
    )

# Footer
st.markdown("""
<div class='small'>
⚠️ 안내: MBTI는 자기이해를 돕는 하나의 렌즈일 뿐, 진로를 단정하지 않아요. 다양한 경험과 데이터로 나만의 경로를 만들어가요! 🌱
</div>
""", unsafe_allow_html=True)
