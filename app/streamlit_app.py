from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="CGV 리뷰 파일럿 분석",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# 최소 CSS
# -----------------------------
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    .theory-card {
        padding: 1rem 1rem 0.8rem 1rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        background-color: #fafafa;
        height: 100%;
    }

    .question-card {
        padding: 1rem 1rem 0.8rem 1rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.95rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 경로
# -----------------------------
APP_DIR = Path(__file__).resolve().parent
ROOT = APP_DIR.parent

POSTER_PATH = ROOT / "assets" / "images" / "movie_poster.jpg"
SUMMARY_PATH = ROOT / "outputs" / "tables" / "summary_statistics.csv"

# -----------------------------
# 데이터 로드
# -----------------------------
@st.cache_data
def load_summary(path: Path) -> dict:
    if not path.exists():
        return {}

    df = pd.read_csv(path)
    if {"metric", "value"}.issubset(df.columns):
        return dict(zip(df["metric"], df["value"]))
    return {}


summary = load_summary(SUMMARY_PATH)

total_reviews = int(float(summary.get("total_reviews", 46600)))
positive_reviews = int(float(summary.get("positive_reviews", 0)))
negative_reviews = int(float(summary.get("negative_reviews", 0)))
positive_ratio = float(summary.get("positive_ratio", 0)) * 100 if "positive_ratio" in summary else 0.0

# -----------------------------
# 제목
# -----------------------------
st.title("CGV 영화 리뷰 데이터 기반 관객 반응 초기 분석")
st.caption("(차경진 교수님 공유용 파일럿 버전 · 저장된 결과를 불러와 시각화하는 1차 Streamlit 구성)")

# -----------------------------
# 안내 박스
# -----------------------------
st.info(
    "리뷰 크롤링은 **2026-03-30 00:18**에 시작되었으며, "
    "**2026-04-01 현재까지도 계속 진행 중**입니다. "
    f"현재 화면의 1차 분석 결과는 중간 저장 결과인 46,600건 중 결측치 1건을 제외한 **{total_reviews:,}건**의 리뷰 데이터를 기준으로 정리했습니다."
)

# -----------------------------
# 소개 + 포스터
# -----------------------------
col1, col2 = st.columns([1.6, 1.0], gap="large")

with col1:
    st.markdown("## 프로젝트 소개")
    st.write(
        """
        본 프로젝트는 CGV 영화 리뷰 데이터를 바탕으로 관객 반응의 정서적 분포,
        시계열 변화, 그리고 긍정·부정 담론의 핵심 표현을 분석한 초기 Streamlit 대시보드입니다.

        특히 본 분석은 단순히 “평가가 좋은가, 나쁜가”를 보는 데 그치지 않고,
        높은 사회적 기대와 실제 관람 경험 사이의 간극,
        그리고 디지털 플랫폼 위에서 형성되는 집단적 반응 구조를 함께 해석해보고자 합니다.
        """
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("현재 분석 리뷰 수", f"{total_reviews:,}")
    m2.metric("긍정 리뷰 수", f"{positive_reviews:,}")
    m3.metric("부정 리뷰 수", f"{negative_reviews:,}")
    m4.metric("긍정 비율", f"{positive_ratio:.2f}%")

with col2:
    if POSTER_PATH.exists():
        st.image(str(POSTER_PATH), caption="영화 <왕과 사는 남자> 포스터", use_container_width=True)
    else:
        st.warning("포스터 이미지를 찾을 수 없습니다: assets/images/movie_poster.jpg")

st.markdown("---")

# -----------------------------
# 연구 질문
# -----------------------------
st.markdown("## 연구 질문")

rq1, rq2, rq3 = st.columns(3, gap="large")

with rq1:
    st.markdown(
        """
        <div class="question-card">
        <h4>1. 전체 반응은 얼마나 긍정적인가?</h4>
        <p>
        리뷰 전반의 감성 분포를 통해 관객 반응의 기본 구조를 확인합니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rq2:
    st.markdown(
        """
        <div class="question-card">
        <h4>2. 반응은 시간에 따라 어떻게 달라지는가?</h4>
        <p>
        날짜별 긍정 비율과 리뷰 수 변화를 통해 시계열적 흐름을 살펴봅니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rq3:
    st.markdown(
        """
        <div class="question-card">
        <h4>3. 긍정과 부정은 무엇을 중심으로 형성되는가?</h4>
        <p>
        핵심 키워드와 표현을 바탕으로 담론 구조를 비교합니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 이론적 해석 가능성
# -----------------------------
st.markdown("## 이론적 해석 가능성")

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown(
        """
        <div class="theory-card">
        <h4>기대불일치 이론</h4>
        <p>
        관객은 관람 전에 이미 기대를 형성합니다.
        실제 경험이 기대에 미치지 못하면 실망이 발생할 수 있으며,
        일부 부정 리뷰는 절대적 품질보다 <b>기대 대비 아쉬움</b>을 반영할 수 있습니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="theory-card">
        <h4>사회적 증거 / 밴드왜건 효과</h4>
        <p>
        많은 추천, 높은 화제성, 강한 입소문은
        후기 관객의 기대 수준을 끌어올릴 수 있습니다.
        따라서 평가는 작품 자체뿐 아니라 <b>사회적으로 형성된 기대</b>의 영향도 받을 수 있습니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="theory-card">
        <h4>플랫폼 리뷰 데이터의 방법론적 의미</h4>
        <p>
        온라인 리뷰는 자발적으로 생성된 대규모 텍스트 데이터입니다.
        설문과 달리 실시간 반응과 표현 양상을 포착할 수 있어,
        집단적 감정과 담론 구조를 읽는 자료가 됩니다.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 다음 페이지 안내
# -----------------------------
st.markdown("## 다음 페이지에서 확인할 내용")
st.markdown(
    f"""
    - 전체 리뷰 수 **{total_reviews:,}건** 기준 요약 지표  
    - 날짜별 리뷰 수 변화와 긍정 비율 추이  
    - 초반·중반·후반 비교를 통한 시기별 반응 차이  
    - 긍정 담론의 중심: **배우 연기, 감정적 여운**  
    - 부정 담론의 중심: **스토리, 연출, 기대 대비 아쉬움**
    """
)

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1, 1.2, 1])

with center:
    if st.button("분석 결과 보기", use_container_width=True, type="primary"):
        st.switch_page("pages/01_분석결과.py")