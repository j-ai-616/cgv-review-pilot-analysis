from pathlib import Path
import pandas as pd
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="CGV 리뷰 분석 | 왕과 사는 남자",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        max-width: 1150px;
    }

    .hero-box {
        padding: 2rem 2rem 1.6rem 2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #111827 0%, #374151 100%);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #e5e7eb;
        line-height: 1.7;
    }

    .section-title {
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }

    .summary-card {
        padding: 1.1rem 1.1rem 0.9rem 1.1rem;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
    }

    .topic-card {
        padding: 1rem 1rem 0.85rem 1rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background-color: #fafafa;
        height: 100%;
    }

    .theory-card {
        padding: 1rem 1rem 0.85rem 1rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
    }

    .question-card {
        padding: 1rem 1rem 0.85rem 1rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background-color: #f9fafb;
        height: 100%;
    }

    .insight-box {
        padding: 1.1rem 1.2rem;
        border-radius: 18px;
        border-left: 6px solid #374151;
        background-color: #f9fafb;
        line-height: 1.7;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.94rem;
        line-height: 1.6;
    }

    .center-text {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 경로 설정
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

# 최종 분석 결과 기준값
total_reviews = int(float(summary.get("total_reviews", 49010)))
positive_ratio = float(summary.get("positive_ratio", 0.9707)) * 100
negative_ratio = 100 - positive_ratio

positive_reviews = int(float(summary.get("positive_reviews", round(total_reviews * positive_ratio / 100))))
negative_reviews = int(float(summary.get("negative_reviews", total_reviews - positive_reviews)))

# -----------------------------
# Hero
# -----------------------------
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">영화 &lt;왕과 사는 남자&gt; CGV 리뷰 분석</div>
        <div class="hero-subtitle">
            감성 분포와 BERTopic 기반 토픽 구조를 활용해 관객 반응의 전체 흐름,
            긍정·부정 담론의 차이, 그리고 플랫폼 리뷰 데이터가 보여주는 집단적 반응 구조를 분석한 프로젝트입니다.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 소개 + 포스터
# -----------------------------
col1, col2 = st.columns([1.6, 1.0], gap="large")

with col1:
    st.markdown('<div class="section-title">프로젝트 개요</div>', unsafe_allow_html=True)

    st.write(
        """
        본 프로젝트는 영화 **<왕과 사는 남자>**에 대한 CGV 관객 리뷰를 수집하고,
        텍스트 전처리, 감성 라벨 분석, BERTopic 기반 토픽 모델링을 수행한 영화 리뷰 텍스트 분석 프로젝트입니다.

        분석의 목적은 단순히 영화가 긍정적으로 평가되었는지 확인하는 데 그치지 않고,
        관객들이 어떤 표현과 주제를 중심으로 영화를 해석했는지 구조적으로 살펴보는 데 있습니다.
        """
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("분석 리뷰 수", f"{total_reviews:,}건")
    m2.metric("분석 기간", "2026.02.05 ~ 03.29")
    m3.metric("긍정 비율", f"{positive_ratio:.2f}%")
    m4.metric("부정 비율", f"{negative_ratio:.2f}%")

with col2:
    if POSTER_PATH.exists():
        st.image(
            str(POSTER_PATH),
            caption="영화 <왕과 사는 남자> 포스터",
            use_container_width=True,
        )
    else:
        st.warning("포스터 이미지를 찾을 수 없습니다: assets/images/movie_poster.jpg")

st.markdown("---")

# -----------------------------
# 핵심 분석 결과
# -----------------------------
st.markdown('<div class="section-title">핵심 분석 결과</div>', unsafe_allow_html=True)

r1, r2, r3 = st.columns(3, gap="large")

with r1:
    st.markdown(
        f"""
        <div class="summary-card">
            <h4>감성 분포</h4>
            <p>
            전체 리뷰 중 긍정 리뷰 비율은 <b>{positive_ratio:.2f}%</b>로,
            관객 반응은 전반적으로 매우 긍정적인 방향으로 형성되었습니다.
            </p>
            <p class="small-muted">
            긍정 리뷰 수: {positive_reviews:,}건<br>
            부정 리뷰 수: {negative_reviews:,}건
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r2:
    st.markdown(
        """
        <div class="summary-card">
            <h4>주요 호평 축</h4>
            <p>
            BERTopic 결과, 가장 큰 반응 축은
            <b>배우 연기와 감동 중심의 전반적 호평</b>으로 확인되었습니다.
            </p>
            <p class="small-muted">
            관객들은 배우의 연기, 감정선, 몰입감, 여운을 중심으로 긍정적 평가를 남겼습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with r3:
    st.markdown(
        """
        <div class="summary-card">
            <h4>구체적 아쉬움</h4>
            <p>
            전체적으로 긍정 반응이 압도적이었지만,
            <b>호랑이 CG에 대한 아쉬움</b>도 독립된 토픽으로 도출되었습니다.
            </p>
            <p class="small-muted">
            이는 단순한 부정 평가가 아니라 특정 요소에 대한 세부적 관객 반응으로 해석할 수 있습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 연구 질문
# -----------------------------
st.markdown('<div class="section-title">연구 질문</div>', unsafe_allow_html=True)

rq1, rq2, rq3 = st.columns(3, gap="large")

with rq1:
    st.markdown(
        """
        <div class="question-card">
            <h4>1. 전체 관객 반응은 얼마나 긍정적인가?</h4>
            <p>
            감성 라벨 분석을 통해 리뷰 전반의 긍정·부정 분포를 확인합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rq2:
    st.markdown(
        """
        <div class="question-card">
            <h4>2. 관객 반응은 어떤 주제로 나뉘는가?</h4>
            <p>
            BERTopic을 활용해 리뷰 텍스트에 내재된 주요 담론 구조를 도출합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with rq3:
    st.markdown(
        """
        <div class="question-card">
            <h4>3. 긍정과 아쉬움은 무엇을 중심으로 형성되는가?</h4>
            <p>
            배우 연기, 감동, 한국영화 만족감, CG 아쉬움 등 세부 반응을 비교합니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# BERTopic 결과 요약
# -----------------------------
st.markdown('<div class="section-title">BERTopic 주요 토픽 구조</div>', unsafe_allow_html=True)

t1, t2 = st.columns(2, gap="large")

with t1:
    st.markdown(
        """
        <div class="topic-card">
            <h4>Topic 0</h4>
            <p><b>배우 연기와 감동 중심의 전반적 호평</b></p>
            <p class="small-muted">
            가장 큰 리뷰 반응 축으로, 작품 전체에 대한 만족감과 정서적 몰입이 함께 나타납니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with t2:
    st.markdown(
        """
        <div class="topic-card">
            <h4>Topic 1</h4>
            <p><b>유해진·박지훈 연기에 대한 집중 호평</b></p>
            <p class="small-muted">
            특정 배우의 연기력과 캐릭터 표현에 대한 관객의 긍정적 평가가 중심을 이룹니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

t3, t4 = st.columns(2, gap="large")

with t3:
    st.markdown(
        """
        <div class="topic-card">
            <h4>Topic 2</h4>
            <p><b>오랜만에 만족스러운 한국영화라는 반응</b></p>
            <p class="small-muted">
            작품을 개별 영화로만 평가하지 않고, 한국영화 전반에 대한 기대와 비교 속에서 해석하는 반응입니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with t4:
    st.markdown(
        """
        <div class="topic-card">
            <h4>Topic 3</h4>
            <p><b>호랑이 CG에 대한 아쉬움</b></p>
            <p class="small-muted">
            전체적인 호평 속에서도 특정 시각효과 요소에 대한 구체적 아쉬움이 독립적으로 확인되었습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 이론적 해석 가능성
# -----------------------------
st.markdown('<div class="section-title">이론적 해석 가능성</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="large")

with c1:
    st.markdown(
        """
        <div class="theory-card">
            <h4>기대불일치 이론</h4>
            <p>
            관객은 관람 전에 이미 기대를 형성합니다.
            실제 경험이 기대를 충족하거나 초과하면 긍정 평가가 강화되고,
            기대에 미치지 못하면 구체적 아쉬움이 리뷰에 나타날 수 있습니다.
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
            높은 화제성, 추천, 입소문은 후기 관객의 기대 수준을 높일 수 있습니다.
            따라서 리뷰 평가는 작품 자체뿐 아니라 사회적으로 형성된 기대의 영향도 받을 수 있습니다.
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
            온라인 리뷰는 관객이 자발적으로 남긴 대규모 텍스트 데이터입니다.
            설문과 달리 관람 직후의 표현, 감정, 평가 기준을 실시간에 가깝게 포착할 수 있습니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 종합 해석
# -----------------------------
st.markdown('<div class="section-title">종합 해석</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="insight-box">
        이번 분석은 영화 &lt;왕과 사는 남자&gt;에 대한 관객 반응이 단순히 긍정적이었다는 사실을 넘어,
        그 긍정 반응이 <b>배우 연기, 감정적 여운, 한국영화에 대한 만족감</b>을 중심으로 형성되었음을 보여줍니다.
        동시에 <b>호랑이 CG에 대한 아쉬움</b>처럼 구체적이고 세부적인 불만 요인도 독립된 토픽으로 확인되었습니다.
        <br><br>
        따라서 본 프로젝트는 CGV 리뷰 데이터를 활용해 관객 경험을 정량적으로 구조화하고,
        영화 소비자 반응을 감성 분석과 토픽 모델링 관점에서 해석한 파일럿 분석 사례로 볼 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# 다음 페이지 안내
# -----------------------------
st.markdown('<div class="section-title">분석 결과 페이지에서 확인할 내용</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    - 전체 리뷰 **{total_reviews:,}건** 기준 감성 분포
    - 긍정 리뷰와 부정 리뷰의 비율 비교
    - BERTopic 기반 주요 토픽별 리뷰 수
    - 배우 연기, 감동, 한국영화 만족감, CG 아쉬움의 토픽 구조
    - 관객 반응에 대한 종합 해석
    """
)

st.markdown("<br>", unsafe_allow_html=True)

left, center, right = st.columns([1, 1.25, 1])

with center:
    if st.button("분석 결과 보기", use_container_width=True, type="primary"):
        st.switch_page("pages/01_분석결과.py")
