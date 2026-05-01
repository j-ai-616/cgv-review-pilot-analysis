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
    }

    .summary-card {
        padding: 1.05rem 1.15rem 0.95rem 1.15rem;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        background-color: #ffffff;
        height: 100%;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
        line-height: 1.65;
        word-break: keep-all;
    }

    .insight-green {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #eaf7ef;
        color: #166534;
        line-height: 1.65;
        word-break: keep-all;
    }

    .insight-yellow {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #fff7d6;
        color: #854d0e;
        line-height: 1.65;
        word-break: keep-all;
    }

    .analysis-note {
        padding: 1.05rem 1.15rem;
        border-radius: 14px;
        border-left: 6px solid #374151;
        background-color: #f9fafb;
        line-height: 1.75;
        word-break: keep-all;
        margin-top: 0.8rem;
    }

    .blue-note {
        padding: 1rem 1.1rem;
        border-radius: 12px;
        background-color: #eff6ff;
        color: #1d4ed8;
        line-height: 1.65;
        word-break: keep-all;
        margin-top: 1rem;
    }

    .small-muted {
        color: #6b7280;
        font-size: 0.93rem;
        line-height: 1.65;
    }

    .stMetric {
        min-width: 120px;
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

    .plot-caption {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: -0.4rem;
        margin-bottom: 0.6rem;
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
        margin-bottom: 0.5rem;
        font-size: 1.05rem;
        font-weight: 800;
    }

    .footer-list {
        line-height: 1.9;
        word-break: keep-all;
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

PLOTS_DIR = ROOT / "outputs" / "plots"
TABLES_DIR = ROOT / "outputs" / "tables"

# 그래프 파일 후보
PLOT_PATHS = {
    "daily_positive_ratio": [
        PLOTS_DIR / "daily_positive_ratio.png",
        PLOTS_DIR / "daily_sentiment_ratio.png",
        PLOTS_DIR / "positive_ratio_by_date.png",
    ],
    "daily_review_count": [
        PLOTS_DIR / "daily_review_count.png",
        PLOTS_DIR / "review_count_by_date.png",
        PLOTS_DIR / "daily_reviews.png",
    ],
    "period_positive_ratio": [
        PLOTS_DIR / "period_positive_ratio.png",
        PLOTS_DIR / "positive_ratio_by_period.png",
        PLOTS_DIR / "period_sentiment_ratio.png",
    ],
    "period_review_length": [
        PLOTS_DIR / "period_review_length.png",
        PLOTS_DIR / "avg_review_length_by_period.png",
        PLOTS_DIR / "period_avg_review_length.png",
    ],
    "positive_keywords": [
        PLOTS_DIR / "positive_keyword_count.png",
        PLOTS_DIR / "positive_keywords.png",
        PLOTS_DIR / "positive_keyword_bar.png",
    ],
    "negative_keywords": [
        PLOTS_DIR / "negative_keyword_count.png",
        PLOTS_DIR / "negative_keywords.png",
        PLOTS_DIR / "negative_keyword_bar.png",
    ],
    "topic_distribution": [
        PLOTS_DIR / "topic_distribution.png",
        PLOTS_DIR / "bertopic_topic_distribution.png",
        PLOTS_DIR / "topic_count.png",
    ],
}

# 표 파일 후보
TABLE_PATHS = {
    "positive_keywords": [
        TABLES_DIR / "positive_keywords.csv",
        TABLES_DIR / "positive_keyword_count.csv",
        TABLES_DIR / "positive_keyword_table.csv",
    ],
    "negative_keywords": [
        TABLES_DIR / "negative_keywords.csv",
        TABLES_DIR / "negative_keyword_count.csv",
        TABLES_DIR / "negative_keyword_table.csv",
    ],
    "period_keywords": [
        TABLES_DIR / "period_keywords.csv",
        TABLES_DIR / "period_keyword_count.csv",
        TABLES_DIR / "keywords_by_period.csv",
    ],
    "positive_examples": [
        TABLES_DIR / "positive_review_examples.csv",
        TABLES_DIR / "positive_examples.csv",
    ],
    "negative_examples": [
        TABLES_DIR / "negative_review_examples.csv",
        TABLES_DIR / "negative_examples.csv",
    ],
    "topic_info": [
        TABLES_DIR / "topic_info.csv",
        TABLES_DIR / "bertopic_topic_info.csv",
    ],
}

# -----------------------------
# 최종 분석 기준값
# -----------------------------
TOTAL_REVIEWS = 46599
POSITIVE_REVIEWS = 45265
NEGATIVE_REVIEWS = 1334
POSITIVE_RATIO = 97.14
NEGATIVE_RATIO = 2.86
PERIOD = "2026-02-05 ~ 2026-03-29"

TOPIC_SUMMARY = {
    0: "배우 연기와 감동 중심의 전반적 호평",
    1: "유해진·박지훈 연기에 대한 집중 호평",
    2: "오랜만에 만족스러운 한국영화라는 반응",
    3: "호랑이 CG에 대한 아쉬움",
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
def load_csv_if_exists(paths: list[Path]) -> pd.DataFrame:
    path = first_existing(paths)
    if path is None:
        return pd.DataFrame()

    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def show_image_from_candidates(key: str, caption: str | None = None) -> None:
    path = first_existing(PLOT_PATHS[key])
    if path is None:
        st.info(f"그래프 파일을 찾을 수 없습니다: {key}")
        return

    st.image(str(path), use_container_width=True)

    if caption:
        st.markdown(
            f"""
            <div class="plot-caption">{caption}</div>
            """,
            unsafe_allow_html=True,
        )


def normalize_keyword_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df

    rename_map = {}

    for col in df.columns:
        lower = col.lower()
        if lower in ["word", "token", "keyword", "keywords"]:
            rename_map[col] = "keyword"
        elif lower in ["freq", "frequency", "count", "counts"]:
            rename_map[col] = "count"

    df = df.rename(columns=rename_map)

    keep_cols = [col for col in ["period", "sentiment", "keyword", "count"] if col in df.columns]
    if keep_cols:
        df = df[keep_cols]

    return df


def show_dataframe(df: pd.DataFrame, empty_message: str, height: int = 320) -> None:
    if df.empty:
        st.info(empty_message)
    else:
        st.dataframe(df, use_container_width=True, height=height)


# -----------------------------
# 상단
# -----------------------------
top_left, top_right = st.columns([1, 1])

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
m2.metric("긍정 리뷰 수", f"{POSITIVE_REVIEWS:,}")
m3.metric("부정 리뷰 수", f"{NEGATIVE_REVIEWS:,}")
m4.metric("긍정 비율", f"{POSITIVE_RATIO:.2f}%")

st.markdown("<br>", unsafe_allow_html=True)

i1, i2 = st.columns(2, gap="large")

with i1:
    st.markdown(
        """
        <div class="insight-green">
        <b>핵심 메시지 1</b><br>
        전체적으로 긍정 비율이 매우 높게 나타납니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="insight-green">
        <b>핵심 메시지 2</b><br>
        긍정 리뷰에서는 배우 연기와 감정적 여운을 중심으로 한 표현이 두드러집니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with i2:
    st.markdown(
        """
        <div class="insight-yellow">
        <b>핵심 메시지 3</b><br>
        날짜별 긍정 비율 추이에서는 후반부에 소폭 하락 구간이 관찰됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="insight-yellow">
        <b>핵심 메시지 4</b><br>
        부정 리뷰에서는 스토리, 연출, 기대 대비 아쉬움 관련 표현이 상대적으로 더 많이 나타납니다.
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
    show_image_from_candidates(
        "daily_positive_ratio",
        "날짜별 긍정 비율 변화",
    )

with col2:
    st.subheader("날짜별 리뷰 수 변화")
    show_image_from_candidates(
        "daily_review_count",
        "날짜별 리뷰 수 변화",
    )

st.markdown(
    """
    <div class="analysis-note">
    <b>해석 포인트</b><br>
    전체 평균만 보면 매우 긍정적인 작품처럼 보이지만, 날짜별 추이를 함께 보면 일부 후반부 구간에서
    긍정 비율이 다소 흔들리는 구간을 확인할 수 있습니다. 이는 영화 평가가 고정된 하나의 수치가 아니라,
    관람 시점과 누적된 입소문에 따라 달라질 수 있음을 보여줍니다.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("날짜별 요약 보기"):
    st.write(
        """
        날짜별 리뷰 수와 긍정 비율은 영화 개봉 이후 관객 반응이 어떻게 확산되고 변화했는지 보여주는 지표입니다.
        리뷰 수가 많은 시기에는 대중적 관심이 집중되었고, 긍정 비율의 변화는 관객 기대와 실제 관람 경험의 차이를
        간접적으로 보여줄 수 있습니다.
        """
    )

st.markdown("---")

# -----------------------------
# 2. 초반·중반·후반 비교
# -----------------------------
st.header("2. 초반·중반·후반 비교")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.subheader("시기별 긍정 비율")
    show_image_from_candidates(
        "period_positive_ratio",
        "초반·중반·후반 긍정 비율 비교",
    )

with col2:
    st.subheader("시기별 평균 리뷰 길이")
    show_image_from_candidates(
        "period_review_length",
        "초반·중반·후반 평균 리뷰 길이 비교",
    )

st.markdown(
    """
    <div class="analysis-note">
    <b>해석 포인트</b><br>
    시기별 비교는 단순히 리뷰 수의 차이만 보는 것이 아니라, 작품을 둘러싼 기대와 반응의 흐름이
    어떻게 이동하는지를 보여줍니다. 특히 후반부의 소폭 변화는 사회적 기대와 실제 경험 사이의 간극 가능성을
    시사합니다.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("시기별 요약 보기"):
    st.write(
        """
        초반 리뷰는 개봉 직후의 기대와 관심을 반영하는 경향이 있고,
        중반 리뷰는 입소문과 추천의 영향을 받을 수 있습니다.
        후반 리뷰는 이미 형성된 평가를 접한 관객들의 기대와 비교 속에서 작성될 가능성이 있습니다.
        """
    )

st.markdown("---")

# -----------------------------
# 3. 긍정·부정 담론 구조
# -----------------------------
st.header("3. 긍정·부정 담론 구조")

tab_pos, tab_neg, tab_topic = st.tabs(["긍정 키워드", "부정 키워드", "토픽 분포"])

with tab_pos:
    st.subheader("긍정 리뷰 핵심 표현")

    col1, col2 = st.columns([1.35, 1.0], gap="large")

    with col1:
        show_image_from_candidates(
            "positive_keywords",
            "긍정 리뷰 상위 키워드",
        )

    with col2:
        positive_keywords = normalize_keyword_table(
            load_csv_if_exists(TABLE_PATHS["positive_keywords"])
        )
        show_dataframe(
            positive_keywords.head(15),
            "긍정 키워드 표 파일을 찾을 수 없습니다.",
            height=380,
        )

    st.markdown(
        """
        <div class="blue-note">
        긍정 담론의 중심은 배우 연기, 감정적 여운, 몰입 경험으로 해석할 수 있습니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_neg:
    st.subheader("부정 리뷰 핵심 표현")

    col1, col2 = st.columns([1.35, 1.0], gap="large")

    with col1:
        show_image_from_candidates(
            "negative_keywords",
            "부정 리뷰 상위 키워드",
        )

    with col2:
        negative_keywords = normalize_keyword_table(
            load_csv_if_exists(TABLE_PATHS["negative_keywords"])
        )
        show_dataframe(
            negative_keywords.head(15),
            "부정 키워드 표 파일을 찾을 수 없습니다.",
            height=380,
        )

    st.markdown(
        """
        <div class="blue-note">
        부정 담론은 스토리, 연출, 기대 대비 아쉬움처럼 특정 요소에 대한 세부 평가와 연결됩니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_topic:
    st.subheader("BERTopic 토픽 분포")

    col1, col2 = st.columns([1.25, 1.0], gap="large")

    with col1:
        show_image_from_candidates(
            "topic_distribution",
            "BERTopic 주요 토픽별 리뷰 수",
        )

    with col2:
        for topic_id, topic_text in TOPIC_SUMMARY.items():
            st.markdown(
                f"""
                <div class="topic-card">
                    <h4>Topic {topic_id}</h4>
                    <p>{topic_text}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height: 0.7rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="blue-note">
        BERTopic 결과는 관객 반응이 하나의 긍정/부정 구분으로만 설명되지 않고,
        배우 연기, 감동, 한국영화 만족감, CG 아쉬움 등 여러 담론 축으로 구성되어 있음을 보여줍니다.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# -----------------------------
# 4. 시기별 키워드 비교
# -----------------------------
st.header("4. 시기별 키워드 비교")

period_keywords = normalize_keyword_table(
    load_csv_if_exists(TABLE_PATHS["period_keywords"])
)

show_dataframe(
    period_keywords.head(30),
    "시기별 키워드 표 파일을 찾을 수 없습니다.",
    height=420,
)

st.markdown(
    """
    <div class="analysis-note">
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
    positive_examples = load_csv_if_exists(TABLE_PATHS["positive_examples"])
    show_dataframe(
        positive_examples.head(10),
        "긍정 리뷰 예시 파일을 찾을 수 없습니다.",
        height=360,
    )

with tab_neg_review:
    negative_examples = load_csv_if_exists(TABLE_PATHS["negative_examples"])
    show_dataframe(
        negative_examples.head(10),
        "부정 리뷰 예시 파일을 찾을 수 없습니다.",
        height=360,
    )

st.markdown(
    """
    <div class="analysis-note">
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
    전체 {TOTAL_REVIEWS:,}건의 리뷰 중 긍정 리뷰는 {POSITIVE_REVIEWS:,}건으로,
    긍정 비율은 {POSITIVE_RATIO:.2f}%입니다. 이는 관객 반응이 전반적으로 높은 만족도를 보였음을 의미합니다.
    <br><br>

    <b>2. 긍정 반응의 중심은 배우 연기와 감정적 몰입입니다.</b><br>
    긍정 리뷰에서는 배우, 연기, 감동, 여운과 같은 표현이 두드러지며,
    작품의 정서적 설득력이 긍정 평가의 핵심 기반으로 작용한 것으로 해석할 수 있습니다.
    <br><br>

    <b>3. 부정 반응은 특정 요소에 대한 아쉬움으로 나타납니다.</b><br>
    전체적인 호평 속에서도 스토리, 연출, CG, 기대 대비 아쉬움과 같은 표현이 부정 담론에서 확인됩니다.
    특히 호랑이 CG에 대한 아쉬움은 BERTopic 결과에서도 독립된 토픽으로 확인됩니다.
    <br><br>

    <b>4. 시계열적으로는 후반부에서 소폭 하락 구간이 보입니다.</b><br>
    이는 누적된 입소문과 사회적 기대가 관객의 실제 관람 경험과 만나면서 평가의 기준이 달라질 수 있음을 보여줍니다.
    <br><br>

    <b>5. 본 파일럿 버전은 저장된 결과를 시각적으로 정리한 1차 대시보드입니다.</b><br>
    향후 최종 데이터 확보와 추가 모델링을 통해 BERTopic 결과, 감성 분석 기준, 시계열 해석을 더 정교하게 확장할 수 있습니다.
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
