from pathlib import Path

import pandas as pd
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="분석 결과 | CGV 리뷰 분석",
    page_icon="📊",
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
        padding-top: 3.2rem;
        padding-bottom: 3rem;
        max-width: 1120px;
    }

    h1, h2, h3 {
        letter-spacing: -0.03em;
    }

    hr {
        margin: 2.2rem 0;
    }

    .page-caption {
        color: #6b7280;
        font-size: 0.95rem;
        margin-top: -0.5rem;
        margin-bottom: 1.6rem;
        word-break: keep-all;
    }

    .note-box {
        padding: 1.05rem 1.15rem;
        border-radius: 14px;
        border-left: 6px solid #374151;
        background-color: #f9fafb;
        line-height: 1.75;
        word-break: keep-all;
        margin-top: 0.8rem;
    }

    .green-box {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #eaf7ef;
        color: #166534;
        line-height: 1.65;
        word-break: keep-all;
    }

    .yellow-box {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #fff7d6;
        color: #854d0e;
        line-height: 1.65;
        word-break: keep-all;
    }

    .blue-box {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #eff6ff;
        color: #1d4ed8;
        line-height: 1.65;
        word-break: keep-all;
        margin-top: 1rem;
    }

    .topic-card {
        padding: 1rem 1.1rem;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
        line-height: 1.65;
        word-break: keep-all;
    }

    .topic-card h4 {
        margin-top: 0;
        margin-bottom: 0.45rem;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .plot-caption {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: -0.3rem;
        margin-bottom: 0.6rem;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.93rem;
        line-height: 1.65;
    }

    .footer-list {
        line-height: 1.9;
        word-break: keep-all;
    }

    [data-testid="stMetricValue"] {
        font-size: 1.55rem;
        white-space: nowrap;
    }

    [data-testid="stMetricLabel"] {
        white-space: nowrap;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 1.25rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 경로 설정
# -----------------------------
APP_DIR = Path(__file__).resolve().parent
APP_ROOT = APP_DIR.parent
ROOT = APP_ROOT.parent

FIGURES_DIR = ROOT / "outputs" / "figures"
TABLES_DIR = ROOT / "outputs" / "tables"

# -----------------------------
# 최종 분석 기준값
# -----------------------------
TOTAL_REVIEWS = 49010
POSITIVE_RATIO = 97.07
NEGATIVE_RATIO = 100 - POSITIVE_RATIO
POSITIVE_REVIEWS = round(TOTAL_REVIEWS * POSITIVE_RATIO / 100)
NEGATIVE_REVIEWS = TOTAL_REVIEWS - POSITIVE_REVIEWS
PERIOD = "2026-02-05 ~ 2026-03-29"

# -----------------------------
# 산출물 파일 후보
# -----------------------------
FIGURE_PATHS = {
    "daily_positive_ratio": [
        FIGURES_DIR / "positive_ratio_by_date.png",
    ],
    "daily_review_count": [
        FIGURES_DIR / "review_count_by_date.png",
    ],
    "period_positive_ratio": [
        FIGURES_DIR / "refined_positive_ratio_by_period.png",
    ],
    "period_review_length": [
        FIGURES_DIR / "refined_avg_review_length_by_period.png",
        FIGURES_DIR / "avg_review_length_by_date.png",
    ],
    "positive_keywords": [
        FIGURES_DIR / "refined_top_keywords_bar.png",
        FIGURES_DIR / "top_keywords_bar.png",
    ],
    "negative_keywords": [
        FIGURES_DIR / "refined_negative_keywords_bar.png",
    ],
    "bigram": [
        FIGURES_DIR / "refined_bigram_bar.png",
        FIGURES_DIR / "bigram_bar.png",
    ],
    "tfidf": [
        FIGURES_DIR / "refined_top_tfidf_terms.png",
        FIGURES_DIR / "top_tfidf_terms.png",
    ],
}

TABLE_PATHS = {
    "daily_trend": [
        TABLES_DIR / "daily_trend.csv",
        TABLES_DIR / "daily_trend_from_notebook.csv",
    ],
    "positive_keywords": [
        TABLES_DIR / "refined_positive_top_keywords.csv",
        TABLES_DIR / "top_keywords_positive.csv",
    ],
    "negative_keywords": [
        TABLES_DIR / "refined_negative_top_keywords.csv",
        TABLES_DIR / "top_keywords_negative.csv",
    ],
    "period_keywords": [
        TABLES_DIR / "refined_period_keywords.csv",
    ],
    "period_summary": [
        TABLES_DIR / "refined_period_summary.csv",
    ],
    "positive_examples": [
        TABLES_DIR / "refined_positive_long_samples.csv",
        TABLES_DIR / "positive_review_samples.csv",
    ],
    "negative_examples": [
        TABLES_DIR / "refined_negative_long_samples.csv",
        TABLES_DIR / "negative_review_samples.csv",
    ],
    "bigrams": [
        TABLES_DIR / "refined_bigrams.csv",
        TABLES_DIR / "bigrams.csv",
    ],
}


# -----------------------------
# 유틸 함수
# -----------------------------
def first_existing(paths: list[Path]) -> Path | None:
    for path in paths:
        if path.exists():
            return path
    return None


@st.cache_data
def load_csv(path_str: str) -> pd.DataFrame:
    path = Path(path_str)
    if not path.exists():
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def load_table(key: str) -> pd.DataFrame:
    path = first_existing(TABLE_PATHS[key])
    if path is None:
        return pd.DataFrame()
    return load_csv(str(path))


def show_figure(key: str, caption: str) -> None:
    path = first_existing(FIGURE_PATHS[key])
    if path is None:
        st.info("시각화 결과를 준비 중입니다.")
        return

    st.image(str(path), use_container_width=True)
    st.markdown(
        f"""
        <div class="plot-caption">{caption}</div>
        """,
        unsafe_allow_html=True,
    )


def normalize_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    rename_map = {}
    for col in df.columns:
        lower = col.lower()

        if lower in ["word", "token", "keyword", "keywords", "term"]:
            rename_map[col] = "keyword"
        elif lower in ["freq", "frequency", "count", "counts"]:
            rename_map[col] = "count"
        elif lower in ["review", "text", "content", "review_text"]:
            rename_map[col] = "review"

    return df.rename(columns=rename_map)


def show_table(df: pd.DataFrame, empty_message: str, height: int = 340) -> None:
    if df.empty:
        st.info(empty_message)
    else:
        st.dataframe(df, use_container_width=True, height=height)


# -----------------------------
# 상단
# -----------------------------
top_left, _ = st.columns([1.1, 1.9])

with top_left:
    if st.button("← 소개 페이지로 돌아가기", use_container_width=True):
        st.switch_page("streamlit_app.py")

st.title("분석 결과")
st.markdown(
    """
    <div class="page-caption">
    CGV 리뷰 데이터 기반 감성 분포, 시계열 변화, 키워드 구조, BERTopic 결과 요약
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# 핵심 요약
# -----------------------------
st.header("핵심 요약")

m1, m2, m3, m4 = st.columns(4)
m1.metric("총 리뷰 수", f"{TOTAL_REVIEWS:,}")
m2.metric("긍정 리뷰 수", f"약 {POSITIVE_REVIEWS:,}")
m3.metric("부정 리뷰 수", f"약 {NEGATIVE_REVIEWS:,}")
m4.metric("긍정 비율", f"{POSITIVE_RATIO:.2f}%")

st.markdown(
    f"""
    <div class="small-muted">
    분석 기간: <b>{PERIOD}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

i1, i2 = st.columns(2, gap="large")

with i1:
    st.markdown(
        """
        <div class="green-box">
        <b>핵심 메시지 1</b><br>
        전체적으로 긍정 비율이 매우 높게 나타납니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="green-box">
        <b>핵심 메시지 2</b><br>
        긍정 리뷰에서는 배우 연기와 감정적 여운을 중심으로 한 표현이 두드러집니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with i2:
    st.markdown(
        """
        <div class="yellow-box">
        <b>핵심 메시지 3</b><br>
        관객 반응은 단순한 긍정·부정 구분을 넘어 여러 담론 축으로 구성됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="yellow-box">
        <b>핵심 메시지 4</b><br>
        호랑이 CG에 대한 아쉬움처럼 구체적 요소에 대한 세부 반응도 독립적으로 확인됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 1. 시계열 변화
# -----------------------------
st.header("1. 시계열적 관객 반응 변화")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("날짜별 긍정 비율 추이")
    show_figure("daily_positive_ratio", "날짜별 긍정 비율 변화")

with col2:
    st.subheader("날짜별 리뷰 수 변화")
    show_figure("daily_review_count", "날짜별 리뷰 수 변화")

st.markdown(
    """
    <div class="note-box">
    <b>해석 포인트</b><br>
    전체 평균만 보면 매우 긍정적인 작품처럼 보이지만, 날짜별 추이를 함께 보면 관객 반응이
    시간에 따라 조금씩 달라질 수 있음을 확인할 수 있습니다. 이는 영화 평가가 고정된 하나의 수치가 아니라,
    관람 시점과 누적된 입소문에 따라 변화할 수 있음을 보여줍니다.
    </div>
    """,
    unsafe_allow_html=True,
)

daily_trend = normalize_table(load_table("daily_trend"))

with st.expander("날짜별 데이터 표 보기"):
    show_table(daily_trend, "날짜별 추이 표를 준비 중입니다.", height=360)

st.markdown("---")

# -----------------------------
# 2. 초반·중반·후반 비교
# -----------------------------
st.header("2. 초반·중반·후반 비교")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("시기별 긍정 비율")
    show_figure("period_positive_ratio", "초반·중반·후반 긍정 비율 비교")

with col2:
    st.subheader("시기별 평균 리뷰 길이")
    show_figure("period_review_length", "초반·중반·후반 평균 리뷰 길이 비교")

st.markdown(
    """
    <div class="note-box">
    <b>해석 포인트</b><br>
    시기별 비교는 단순히 리뷰 수의 차이만 보는 것이 아니라, 작품을 둘러싼 기대와 반응의 흐름이
    어떻게 이동하는지를 보여줍니다. 초반·중반·후반의 차이는 관객 기대와 실제 관람 경험 사이의
    관계를 해석하는 단서가 됩니다.
    </div>
    """,
    unsafe_allow_html=True,
)

period_summary = normalize_table(load_table("period_summary"))

with st.expander("시기별 요약 표 보기"):
    show_table(period_summary, "시기별 요약 표를 준비 중입니다.", height=260)

st.markdown("---")

# -----------------------------
# 3. 긍정·부정 담론 구조
# -----------------------------
st.header("3. 긍정·부정 담론 구조")

tab_pos, tab_neg, tab_bigram, tab_tfidf, tab_topic = st.tabs(
    ["긍정 키워드", "부정 키워드", "결합 표현", "TF-IDF", "BERTopic 요약"]
)

with tab_pos:
    st.subheader("긍정 리뷰 핵심 표현")

    col1, col2 = st.columns([1.35, 1.0], gap="large")

    with col1:
        show_figure("positive_keywords", "긍정 리뷰 상위 키워드")

    with col2:
        positive_keywords = normalize_table(load_table("positive_keywords"))
        show_table(
            positive_keywords.head(20),
            "긍정 키워드 표를 준비 중입니다.",
            height=390,
        )

    st.markdown(
        """
        <div class="blue-box">
        긍정 담론의 중심은 배우 연기, 감정적 여운, 몰입 경험으로 해석할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_neg:
    st.subheader("부정 리뷰 핵심 표현")

    col1, col2 = st.columns([1.35, 1.0], gap="large")

    with col1:
        show_figure("negative_keywords", "부정 리뷰 상위 키워드")

    with col2:
        negative_keywords = normalize_table(load_table("negative_keywords"))
        show_table(
            negative_keywords.head(20),
            "부정 키워드 표를 준비 중입니다.",
            height=390,
        )

    st.markdown(
        """
        <div class="blue-box">
        부정 담론은 스토리, 연출, 기대 대비 아쉬움처럼 특정 요소에 대한 세부 평가와 연결됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_bigram:
    st.subheader("결합 표현 분석")

    col1, col2 = st.columns([1.35, 1.0], gap="large")

    with col1:
        show_figure("bigram", "상위 결합 표현")

    with col2:
        bigrams = normalize_table(load_table("bigrams"))
        show_table(
            bigrams.head(20),
            "결합 표현 표를 준비 중입니다.",
            height=390,
        )

    st.markdown(
        """
        <div class="blue-box">
        단어 하나가 아니라 함께 등장하는 표현을 보면, 관객이 어떤 맥락에서 작품을 평가했는지 더 구체적으로 파악할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_tfidf:
    st.subheader("TF-IDF 핵심 표현")

    show_figure("tfidf", "TF-IDF 기준 주요 표현")

    st.markdown(
        """
        <div class="blue-box">
        TF-IDF는 단순 빈도보다 특정 리뷰 집합에서 상대적으로 두드러지는 표현을 확인하는 데 유용합니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_topic:
    st.subheader("BERTopic 주요 토픽 구조")

    t1, t2 = st.columns(2, gap="large")

    with t1:
        st.markdown(
            """
            <div class="topic-card">
            <h4>Topic 0</h4>
            <p><b>배우 연기와 감동 중심의 전반적 호평</b></p>
            <p class="small-muted">가장 큰 리뷰 반응 축으로, 작품 전체에 대한 만족감과 정서적 몰입이 함께 나타납니다.</p>
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
            <p class="small-muted">특정 배우의 연기력과 캐릭터 표현에 대한 관객의 긍정적 평가가 중심을 이룹니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    t3, t4 = st.columns(2, gap="large")

    with t3:
        st.markdown(
            """
            <div class="topic-card">
            <h4>Topic 2</h4>
            <p><b>오랜만에 만족스러운 한국영화라는 반응</b></p>
            <p class="small-muted">작품을 개별 영화로만 평가하지 않고, 한국영화 전반에 대한 기대와 비교 속에서 해석하는 반응입니다.</p>
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
            <p class="small-muted">전체적인 호평 속에서도 특정 시각효과 요소에 대한 구체적 아쉬움이 독립적으로 확인되었습니다.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="blue-box">
        BERTopic 결과는 관객 반응이 하나의 긍정·부정 구분으로만 설명되지 않고,
        배우 연기, 감동, 한국영화에 대한 만족감, CG 아쉬움 등 여러 담론 축으로 구성되어 있음을 보여줍니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 4. 시기별 키워드 비교
# -----------------------------
st.header("4. 시기별 키워드 비교")

period_keywords = normalize_table(load_table("period_keywords"))

show_table(
    period_keywords.head(40),
    "시기별 키워드 표를 준비 중입니다.",
    height=430,
)

st.markdown(
    """
    <div class="note-box">
    <b>해석 포인트</b><br>
    시기별 키워드를 함께 보면 동일한 작품에 대한 반응도 시간에 따라 강조점이 달라질 수 있음을 확인할 수 있습니다.
    초반에는 기대와 화제성, 중반에는 관람 경험의 공유, 후반에는 누적된 평가와 비교가 더 강하게 반영될 수 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# 5. 대표 리뷰 예시
# -----------------------------
st.header("5. 대표 리뷰 예시")

tab_pos_review, tab_neg_review = st.tabs(["긍정 리뷰 예시", "부정 리뷰 예시"])

with tab_pos_review:
    positive_examples = normalize_table(load_table("positive_examples"))
    show_table(
        positive_examples.head(10),
        "긍정 리뷰 예시를 준비 중입니다.",
        height=380,
    )

with tab_neg_review:
    negative_examples = normalize_table(load_table("negative_examples"))
    show_table(
        negative_examples.head(10),
        "부정 리뷰 예시를 준비 중입니다.",
        height=380,
    )

st.markdown(
    """
    <div class="note-box">
    <b>해석 포인트</b><br>
    대표 리뷰 예시는 정량 분석 결과가 실제 관객 표현 속에서 어떻게 나타나는지 확인하기 위한 보조 자료입니다.
    긍정 리뷰는 연기와 감정적 여운을 중심으로, 부정 리뷰는 특정 장면·연출·기대 대비 아쉬움을 중심으로 구성되는
    경향이 있습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# 6. 종합 해석
# -----------------------------
st.header("6. 종합 해석")

st.markdown(
    f"""
    <div class="footer-list">
    <b>1. 전체 평가는 매우 긍정적입니다.</b><br>
    최종 clean 데이터 {TOTAL_REVIEWS:,}건 기준 긍정 비율은 {POSITIVE_RATIO:.2f}%입니다.
    이는 관객 반응이 전반적으로 높은 만족도를 보였음을 의미합니다.
    <br><br>

    <b>2. 긍정 반응의 중심은 배우 연기와 감정적 몰입입니다.</b><br>
    긍정 리뷰에서는 배우, 연기, 감동, 여운과 같은 표현이 두드러지며,
    작품의 정서적 설득력이 긍정 평가의 핵심 기반으로 작용한 것으로 해석할 수 있습니다.
    <br><br>

    <b>3. 부정 반응은 특정 요소에 대한 아쉬움으로 나타납니다.</b><br>
    전체적인 호평 속에서도 스토리, 연출, CG, 기대 대비 아쉬움과 같은 표현이 부정 담론에서 확인됩니다.
    특히 호랑이 CG에 대한 아쉬움은 BERTopic 결과에서도 독립된 토픽으로 확인됩니다.
    <br><br>

    <b>4. 관객 반응은 여러 토픽 구조로 구성됩니다.</b><br>
    BERTopic 결과는 배우 연기와 감동, 특정 배우에 대한 호평, 한국영화에 대한 만족감,
    CG 아쉬움이라는 복수의 담론 축을 보여줍니다.
    <br><br>

    <b>5. 본 프로젝트는 텍스트 분석 결과를 Streamlit으로 시각화한 사례입니다.</b><br>
    데이터 수집, 전처리, 감성 분석, 키워드 분석, BERTopic 토픽 모델링, 대시보드 구현까지
    하나의 흐름으로 연결했습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# -----------------------------
# 하단 이동 버튼
# -----------------------------
left, center, right = st.columns([1, 1.2, 1])

with center:
    if st.button("소개 페이지로 돌아가기", use_container_width=True):
        st.switch_page("streamlit_app.py")
