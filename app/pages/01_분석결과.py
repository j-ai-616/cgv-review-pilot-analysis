from pathlib import Path
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="CGV 리뷰 분석 결과",
    page_icon="📊",
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
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 한글 폰트 설정
# -----------------------------
def set_korean_font():
    preferred_fonts = [
        "Malgun Gothic",
        "AppleGothic",
        "NanumGothic",
        "Noto Sans CJK KR",
        "Noto Sans KR",
    ]

    available_fonts = {f.name for f in font_manager.fontManager.ttflist}

    for font_name in preferred_fonts:
        if font_name in available_fonts:
            rcParams["font.family"] = font_name
            break

    rcParams["axes.unicode_minus"] = False

set_korean_font()

# -----------------------------
# 경로
# -----------------------------
PAGE_DIR = Path(__file__).resolve().parent
APP_DIR = PAGE_DIR.parent
ROOT = APP_DIR.parent

SUMMARY_PATH = ROOT / "outputs" / "tables" / "summary_statistics.csv"
DAILY_TREND_PATH = ROOT / "outputs" / "tables" / "daily_trend.csv"
PERIOD_SUMMARY_PATH = ROOT / "outputs" / "tables" / "refined_period_summary.csv"
POS_KEYWORDS_PATH = ROOT / "outputs" / "tables" / "refined_positive_top_keywords.csv"
NEG_KEYWORDS_PATH = ROOT / "outputs" / "tables" / "refined_negative_top_keywords.csv"
BIGRAMS_PATH = ROOT / "outputs" / "tables" / "refined_bigrams.csv"
POS_SAMPLES_PATH = ROOT / "outputs" / "tables" / "refined_positive_long_samples.csv"
NEG_SAMPLES_PATH = ROOT / "outputs" / "tables" / "refined_negative_long_samples.csv"
PERIOD_KEYWORDS_PATH = ROOT / "outputs" / "tables" / "refined_period_keywords.csv"

FIG_DIR = ROOT / "outputs" / "figures"
IMG_POS_RATIO_DATE = FIG_DIR / "positive_ratio_by_date.png"
IMG_REVIEW_COUNT_DATE = FIG_DIR / "review_count_by_date.png"
IMG_REFINED_POS_PERIOD = FIG_DIR / "refined_positive_ratio_by_period.png"
IMG_REFINED_LEN_PERIOD = FIG_DIR / "refined_avg_review_length_by_period.png"
IMG_REFINED_KEYWORDS = FIG_DIR / "refined_top_keywords_bar.png"
IMG_REFINED_BIGRAMS = FIG_DIR / "refined_bigram_bar.png"

# -----------------------------
# 유틸
# -----------------------------
@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data
def load_summary(path: Path) -> dict:
    if not path.exists():
        return {}

    df = pd.read_csv(path)
    if {"metric", "value"}.issubset(df.columns):
        return dict(zip(df["metric"], df["value"]))
    return {}

def draw_keyword_bar_chart(df: pd.DataFrame, title: str, top_n: int = 15):
    if df.empty or "keyword" not in df.columns or "count" not in df.columns:
        st.info("그래프를 그릴 키워드 데이터가 없습니다.")
        return

    chart_df = df.head(top_n).copy()
    chart_df = chart_df.sort_values("count", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(chart_df["keyword"], chart_df["count"])
    ax.set_title(title)
    ax.set_xlabel("count")
    ax.set_ylabel("keyword")
    plt.tight_layout()
    st.pyplot(fig, clear_figure=True)

# -----------------------------
# 데이터 로드
# -----------------------------
summary = load_summary(SUMMARY_PATH)
daily_df = load_csv(DAILY_TREND_PATH)
period_df = load_csv(PERIOD_SUMMARY_PATH)
pos_kw_df = load_csv(POS_KEYWORDS_PATH)
neg_kw_df = load_csv(NEG_KEYWORDS_PATH)
bigrams_df = load_csv(BIGRAMS_PATH)
period_keywords_df = load_csv(PERIOD_KEYWORDS_PATH)
pos_samples_df = load_csv(POS_SAMPLES_PATH)
neg_samples_df = load_csv(NEG_SAMPLES_PATH)

total_reviews = int(float(summary.get("total_reviews", 46600)))
positive_reviews = int(float(summary.get("positive_reviews", 0)))
negative_reviews = int(float(summary.get("negative_reviews", 0)))
positive_ratio = float(summary.get("positive_ratio", 0)) * 100 if "positive_ratio" in summary else 0.0
negative_ratio = float(summary.get("negative_ratio", 0)) * 100 if "negative_ratio" in summary else 0.0

# -----------------------------
# 상단
# -----------------------------
top_left, top_mid, top_right = st.columns([1, 1.5, 1])

with top_left:
    if st.button("← 소개 페이지로 돌아가기", use_container_width=True):
        st.switch_page("streamlit_app.py")

with top_mid:
    st.title("분석 결과")
    st.caption("1차 시각화 페이지")

with top_right:
    st.empty()

st.markdown("---")

# -----------------------------
# 핵심 요약
# -----------------------------
st.markdown("## 핵심 요약")

m1, m2, m3, m4 = st.columns(4)
m1.metric("총 리뷰 수", f"{total_reviews:,}")
m2.metric("긍정 리뷰 수", f"{positive_reviews:,}")
m3.metric("부정 리뷰 수", f"{negative_reviews:,}")
m4.metric("긍정 비율", f"{positive_ratio:.2f}%")

c1, c2 = st.columns(2, gap="large")

with c1:
    st.success(
        """
        **핵심 메시지 1**  
        전체적으로 긍정 비율이 매우 높게 나타납니다.
        """
    )
    st.success(
        """
        **핵심 메시지 2**  
        긍정 리뷰에서는 배우 연기와 감정적 여운을 중심으로 한 표현이 두드러집니다.
        """
    )

with c2:
    st.warning(
        """
        **핵심 메시지 3**  
        날짜별 긍정 비율 추이에서는 후반부에 소폭 하락 구간이 관찰됩니다.
        """
    )
    st.warning(
        """
        **핵심 메시지 4**  
        부정 리뷰에서는 스토리, 연출, 기대 대비 아쉬움 관련 표현이 상대적으로 더 많이 보입니다.
        """
    )

st.markdown("---")

# -----------------------------
# 1. 시계열 분석
# -----------------------------
st.markdown("## 1. 시계열적 관객 반응 변화")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 날짜별 긍정 비율 추이")
    if IMG_POS_RATIO_DATE.exists():
        st.image(str(IMG_POS_RATIO_DATE), use_container_width=True)
    else:
        st.warning("positive_ratio_by_date.png 파일이 없습니다.")

with col2:
    st.markdown("### 날짜별 리뷰 수 변화")
    if IMG_REVIEW_COUNT_DATE.exists():
        st.image(str(IMG_REVIEW_COUNT_DATE), use_container_width=True)
    else:
        st.warning("review_count_by_date.png 파일이 없습니다.")

st.markdown(
    """
    **해석 포인트**  
    전체 평균만 보면 매우 긍정적인 작품처럼 보이지만,
    날짜별 추이를 함께 보면 후반부에 반응이 다소 흔들리는 구간이 확인됩니다.
    이는 총평균만으로는 포착하기 어려운 시계열적 반응 변화를 보여줍니다.
    """
)

with st.expander("날짜별 요약표 보기"):
    if not daily_df.empty:
        show_daily = daily_df.copy()
        if "positive_ratio" in show_daily.columns:
            show_daily["positive_ratio"] = (show_daily["positive_ratio"] * 100).round(2)
        if "image_ratio" in show_daily.columns:
            show_daily["image_ratio"] = (show_daily["image_ratio"] * 100).round(2)
        st.dataframe(show_daily, use_container_width=True, hide_index=True)
    else:
        st.info("daily_trend.csv 파일이 없거나 비어 있습니다.")

st.markdown("---")

# -----------------------------
# 2. 시기별 비교
# -----------------------------
st.markdown("## 2. 초반 · 중반 · 후반 비교")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### 시기별 긍정 비율")
    if IMG_REFINED_POS_PERIOD.exists():
        st.image(str(IMG_REFINED_POS_PERIOD), use_container_width=True)
    else:
        st.warning("refined_positive_ratio_by_period.png 파일이 없습니다.")

with col2:
    st.markdown("### 시기별 평균 리뷰 길이")
    if IMG_REFINED_LEN_PERIOD.exists():
        st.image(str(IMG_REFINED_LEN_PERIOD), use_container_width=True)
    else:
        st.warning("refined_avg_review_length_by_period.png 파일이 없습니다.")

with st.expander("시기별 요약표 보기"):
    if not period_df.empty:
        show_period = period_df.copy()
        if "positive_ratio" in show_period.columns:
            show_period["positive_ratio"] = (show_period["positive_ratio"] * 100).round(2)
        if "image_ratio" in show_period.columns:
            show_period["image_ratio"] = (show_period["image_ratio"] * 100).round(2)
        st.dataframe(show_period, use_container_width=True, hide_index=True)
    else:
        st.info("refined_period_summary.csv 파일이 없거나 비어 있습니다.")

st.markdown(
    """
    **해석 포인트**  
    시기별 비교는 단순히 리뷰 수의 차이만 보는 것이 아니라,
    작품을 둘러싼 기대와 반응의 흐름이 어떻게 이동하는지를 보여줍니다.
    특히 후반부의 소폭 변화는 사회적 기대와 실제 경험 사이의 간극 가능성을 시사합니다.
    """
)

st.markdown("---")

# -----------------------------
# 3. 긍정 / 부정 담론 구조
# -----------------------------
st.markdown("## 3. 긍정 · 부정 담론 구조")

tab1, tab2, tab3 = st.tabs(["긍정 키워드", "부정 키워드", "결합 표현(Bigram)"])

with tab1:
    st.markdown("### 긍정 리뷰 핵심 표현")
    col1, col2 = st.columns([1.3, 1.0], gap="large")

    with col1:
        if IMG_REFINED_KEYWORDS.exists():
            st.image(str(IMG_REFINED_KEYWORDS), use_container_width=True)
        else:
            draw_keyword_bar_chart(pos_kw_df, "긍정 리뷰 핵심 표현")

    with col2:
        if not pos_kw_df.empty:
            st.dataframe(pos_kw_df.head(15), use_container_width=True, hide_index=True)
        else:
            st.info("refined_positive_top_keywords.csv 파일이 없거나 비어 있습니다.")

    st.info("긍정 반응의 중심은 배우 연기, 감정적 여운, 몰입 경험으로 해석할 수 있습니다.")

with tab2:
    st.markdown("### 부정 리뷰 핵심 표현")
    col1, col2 = st.columns([1.3, 1.0], gap="large")

    with col1:
        draw_keyword_bar_chart(neg_kw_df, "부정 리뷰 핵심 표현")

    with col2:
        if not neg_kw_df.empty:
            st.dataframe(neg_kw_df.head(15), use_container_width=True, hide_index=True)
        else:
            st.info("refined_negative_top_keywords.csv 파일이 없거나 비어 있습니다.")

    st.info("부정 반응은 스토리, 연출, 기대 대비 아쉬움과 연결되는 표현이 상대적으로 더 자주 나타납니다.")

with tab3:
    st.markdown("### 자주 함께 등장한 표현")
    col1, col2 = st.columns([1.3, 1.0], gap="large")

    with col1:
        if IMG_REFINED_BIGRAMS.exists():
            st.image(str(IMG_REFINED_BIGRAMS), use_container_width=True)
        else:
            st.info("refined_bigram_bar.png 파일이 없습니다.")

    with col2:
        if not bigrams_df.empty:
            st.dataframe(bigrams_df.head(15), use_container_width=True, hide_index=True)
        else:
            st.info("refined_bigrams.csv 파일이 없거나 비어 있습니다.")

    st.info("bigram은 단어 하나보다 더 구체적으로 관객이 무엇을 함께 언급했는지 보여줍니다.")

st.markdown("---")

# -----------------------------
# 4. 시기별 키워드 비교
# -----------------------------
st.markdown("## 4. 시기별 키워드 비교")

period_tabs = st.tabs(["초반", "중반", "후반"])

for period_name, period_tab in zip(["초반", "중반", "후반"], period_tabs):
    with period_tab:
        if not period_keywords_df.empty and "period" in period_keywords_df.columns:
            subset = period_keywords_df[period_keywords_df["period"] == period_name].copy()
            st.dataframe(subset.head(15), use_container_width=True, hide_index=True)
        else:
            st.info("refined_period_keywords.csv 파일이 없거나 period 컬럼이 없습니다.")

st.markdown(
    """
    **해석 포인트**  
    시기별 키워드를 함께 보면 동일한 작품에 대한 반응도 시간에 따라 강조점이 달라질 수 있음을 확인할 수 있습니다.
    """
)

st.markdown("---")

# -----------------------------
# 5. 대표 리뷰 예시
# -----------------------------
st.markdown("## 5. 대표 리뷰 예시")

sample_tab1, sample_tab2 = st.tabs(["긍정 리뷰 예시", "부정 리뷰 예시"])

with sample_tab1:
    if not pos_samples_df.empty:
        show_cols = [col for col in ["review_date", "score", "sentiment_label", "review_length", "review"] if col in pos_samples_df.columns]
        if show_cols:
            st.dataframe(pos_samples_df[show_cols].head(10), use_container_width=True, hide_index=True)
        else:
            st.dataframe(pos_samples_df.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("refined_positive_long_samples.csv 파일이 없거나 비어 있습니다.")

with sample_tab2:
    if not neg_samples_df.empty:
        show_cols = [col for col in ["review_date", "score", "sentiment_label", "review_length", "review"] if col in neg_samples_df.columns]
        if show_cols:
            st.dataframe(neg_samples_df[show_cols].head(10), use_container_width=True, hide_index=True)
        else:
            st.dataframe(neg_samples_df.head(10), use_container_width=True, hide_index=True)
    else:
        st.info("refined_negative_long_samples.csv 파일이 없거나 비어 있습니다.")

st.markdown("---")

# -----------------------------
# 6. 종합 해석
# -----------------------------
st.markdown("## 6. 종합 해석")

st.markdown(
    """
    1. **전체 평가는 매우 긍정적**입니다.  
    다만 전체 평균만으로는 반응의 변화를 충분히 설명하기 어렵습니다.

    2. **시계열적으로 보면 후반부에 소폭 하락 구간**이 보입니다.  
    이는 플랫폼 리뷰가 고정된 평가가 아니라 시간에 따라 움직이는 사회적 반응임을 보여줍니다.

    3. **긍정 담론의 중심은 배우 연기와 감정적 여운**입니다.  
    관객의 호평은 단순 만족보다 감정적 몰입과 배우 퍼포먼스에 강하게 연결됩니다.

    4. **부정 담론은 스토리, 연출, 기대 대비 아쉬움**에 더 가깝습니다.  
    따라서 일부 부정 반응은 작품의 절대적 품질만이 아니라,
    사회적으로 높아진 기대와 실제 관람 경험의 차이에서 비롯될 가능성도 있습니다.

    5. 본 파일럿 버전은 **저장된 결과를 시각적으로 정리한 1차 대시보드**이며,
    향후 최종 데이터 확보 후 BERTopic 등으로 확장할 수 있습니다.
    """
)