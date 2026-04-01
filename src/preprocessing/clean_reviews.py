# project/src/preprocessing/clean_reviews.py

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

import numpy as np
import pandas as pd


# ============================================================
# 기본 설정
# ============================================================

@dataclass
class ReviewPreprocessConfig:
    """
    CGV 리뷰 데이터 전처리 설정값
    """
    csv_path: str = "data/raw/cgv_reviews_checkpoint.csv"
    exclude_partial_dates: bool = True
    partial_dates: tuple[str, ...] = ("2026-03-30",)
    drop_empty_reviews: bool = True
    dedup_col: str = "review_id"


REQUIRED_COLUMNS = [
    "review_id",
    "movie_no",
    "movie_name",
    "author",
    "date",
    "score",
    "like_count",
    "review",
    "movie_kind",
    "has_image",
    "api_start_row",
]


# ============================================================
# 유틸 함수
# ============================================================

def _safe_strip(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip()


def _make_like_bin(series: pd.Series) -> pd.Series:
    return pd.cut(
        series,
        bins=[-1, 0, 1, 3, 5, 10, 20, np.inf],
        labels=["0", "1", "2-3", "4-5", "6-10", "11-20", "21+"]
    )


def _validate_required_columns(df: pd.DataFrame) -> None:
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f"필수 컬럼이 누락되었습니다: {missing_cols}")


# ============================================================
# 로드 함수
# ============================================================

def load_reviews_csv(csv_path: str | Path) -> pd.DataFrame:
    """
    CSV 파일을 읽어 원본 DataFrame을 반환한다.
    """
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {csv_path}")

    df = pd.read_csv(csv_path)
    _validate_required_columns(df)
    return df


# ============================================================
# 품질 점검 함수
# ============================================================

def build_quality_report(df: pd.DataFrame, dedup_col: str = "review_id") -> pd.DataFrame:
    """
    원본 데이터 기준 품질 점검 요약표를 반환한다.
    """
    date_parsed = pd.to_datetime(df["date"], errors="coerce")
    blank_review_mask = df["review"].fillna("").astype(str).str.strip().eq("")

    report = pd.DataFrame({
        "metric": [
            "row_count",
            "column_count",
            "date_parse_fail_count",
            "duplicate_review_id_count",
            "blank_review_count",
            "missing_review_count",
            "missing_score_count",
            "missing_like_count_count",
            "missing_author_count",
        ],
        "value": [
            len(df),
            df.shape[1],
            int(date_parsed.isna().sum()),
            int(df[dedup_col].duplicated().sum()),
            int(blank_review_mask.sum()),
            int(df["review"].isna().sum()),
            int(df["score"].isna().sum()),
            int(df["like_count"].isna().sum()),
            int(df["author"].isna().sum()),
        ]
    })

    return report


# ============================================================
# 전처리 핵심 함수
# ============================================================

def preprocess_reviews(
    df_raw: pd.DataFrame,
    config: Optional[ReviewPreprocessConfig] = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    리뷰 데이터 전처리 수행

    Returns
    -------
    df_text : 전체 텍스트 분석용 데이터
        부분 수집일 포함
    df_time : 날짜 추이 분석용 데이터
        exclude_partial_dates=True면 부분 수집일 제외
    """
    if config is None:
        config = ReviewPreprocessConfig()

    df = df_raw.copy()

    # --------------------------------------------------------
    # 1. 문자열 컬럼 정리
    # --------------------------------------------------------
    str_cols = ["movie_name", "author", "date", "review", "movie_kind", "has_image"]
    for col in str_cols:
        df[col] = _safe_strip(df[col])

    # --------------------------------------------------------
    # 2. 숫자 컬럼 정리
    # --------------------------------------------------------
    num_cols = ["review_id", "movie_no", "score", "like_count", "api_start_row"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # --------------------------------------------------------
    # 3. 날짜 파싱
    # --------------------------------------------------------
    df["dt"] = pd.to_datetime(df["date"], errors="coerce")

    # 날짜 파싱 실패 제거
    df = df.dropna(subset=["dt"]).copy()

    # --------------------------------------------------------
    # 4. 중복 제거
    # --------------------------------------------------------
    df = df.drop_duplicates(subset=[config.dedup_col]).copy()

    # --------------------------------------------------------
    # 5. 빈 리뷰 제거
    # --------------------------------------------------------
    if config.drop_empty_reviews:
        blank_review_mask = df["review"].fillna("").astype(str).str.strip().eq("")
        df = df[~blank_review_mask].copy()

    # --------------------------------------------------------
    # 6. 파생 변수 생성
    # --------------------------------------------------------
    df["review_date"] = df["dt"].dt.date.astype(str)
    df["review_year"] = df["dt"].dt.year
    df["review_month"] = df["dt"].dt.month
    df["review_day"] = df["dt"].dt.day
    df["review_hour"] = df["dt"].dt.hour
    df["review_weekday"] = df["dt"].dt.day_name()

    score_map = {1: "별로예요", 2: "좋았어요"}
    df["sentiment_label"] = df["score"].map(score_map)
    df["is_positive"] = np.where(df["score"] == 2, 1, 0)
    df["is_negative"] = np.where(df["score"] == 1, 1, 0)

    df["has_image_flag"] = np.where(df["has_image"] == "Y", 1, 0)

    df["review_length"] = df["review"].astype(str).str.len()
    df["word_count"] = df["review"].astype(str).str.split().apply(len)

    df["like_bin"] = _make_like_bin(df["like_count"])
    df["is_partial_day"] = df["review_date"].isin(config.partial_dates).astype(int)

    # 날짜별 상대 좋아요 위치
    # 같은 날짜 안에서만 비교하는 보조 지표
    df["like_count_within_date_rank_pct"] = (
        df.groupby("review_date")["like_count"]
        .rank(method="average", pct=True)
    )

    # --------------------------------------------------------
    # 7. 분석용 데이터셋 분리
    # --------------------------------------------------------
    df_text = df.copy()

    if config.exclude_partial_dates:
        df_time = df[~df["review_date"].isin(config.partial_dates)].copy()
    else:
        df_time = df.copy()

    return df_text, df_time


# ============================================================
# 저장 함수
# ============================================================

def save_processed_reviews(
    df_text: pd.DataFrame,
    df_time: pd.DataFrame,
    output_dir: str | Path = "data/processed",
) -> None:
    """
    전처리 결과 저장
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df_text.to_csv(output_dir / "reviews_cleaned_text.csv", index=False, encoding="utf-8-sig")
    df_time.to_csv(output_dir / "reviews_cleaned_time.csv", index=False, encoding="utf-8-sig")


# ============================================================
# 요약 테이블 생성 함수
# ============================================================

def build_summary_statistics(df_text: pd.DataFrame) -> pd.DataFrame:
    """
    기초 통계 요약표 생성
    """
    summary = pd.DataFrame({
        "metric": [
            "total_reviews",
            "positive_reviews",
            "negative_reviews",
            "positive_ratio",
            "negative_ratio",
            "avg_like_count",
            "median_like_count",
            "avg_review_length",
            "median_review_length",
            "image_review_count",
            "image_review_ratio",
            "unique_authors",
            "date_min",
            "date_max",
        ],
        "value": [
            len(df_text),
            int((df_text["score"] == 2).sum()),
            int((df_text["score"] == 1).sum()),
            round(float((df_text["score"] == 2).mean()), 4),
            round(float((df_text["score"] == 1).mean()), 4),
            round(float(df_text["like_count"].mean()), 4),
            round(float(df_text["like_count"].median()), 4),
            round(float(df_text["review_length"].mean()), 4),
            round(float(df_text["review_length"].median()), 4),
            int((df_text["has_image"] == "Y").sum()),
            round(float((df_text["has_image"] == "Y").mean()), 4),
            int(df_text["author"].nunique()),
            str(df_text["dt"].min()),
            str(df_text["dt"].max()),
        ]
    })
    return summary


def build_daily_trend(df_time: pd.DataFrame) -> pd.DataFrame:
    """
    날짜별 추이 테이블 생성
    """
    daily = (
        df_time.groupby("review_date", as_index=False)
        .agg(
            review_count=("review_id", "count"),
            positive_ratio=("is_positive", "mean"),
            avg_like_count=("like_count", "mean"),
            median_like_count=("like_count", "median"),
            avg_review_length=("review_length", "mean"),
            image_ratio=("has_image_flag", "mean"),
        )
        .sort_values("review_date")
        .reset_index(drop=True)
    )
    return daily


def build_image_comparison(df_text: pd.DataFrame) -> pd.DataFrame:
    """
    이미지 포함 여부 비교표 생성
    """
    image_cmp = (
        df_text.groupby("has_image", as_index=False)
        .agg(
            review_count=("review_id", "count"),
            positive_ratio=("is_positive", "mean"),
            avg_like_count=("like_count", "mean"),
            median_like_count=("like_count", "median"),
            avg_review_length=("review_length", "mean"),
            median_review_length=("review_length", "median"),
        )
    )
    return image_cmp


# ============================================================
# 실행 예시
# ============================================================

if __name__ == "__main__":
    # 현재 체크포인트 파일 사용
    config = ReviewPreprocessConfig(
        csv_path="data/raw/cgv_reviews_checkpoint.csv",
        exclude_partial_dates=True,
        partial_dates=("2026-03-30",),
    )

    # 최종 분석 시 아래처럼 바꿔서 사용
    # config = ReviewPreprocessConfig(
    #     csv_path="data/raw/cgv_reviews_final.csv",
    #     exclude_partial_dates=True,
    #     partial_dates=("2026-03-30",),
    # )

    df_raw = load_reviews_csv(config.csv_path)

    quality_report = build_quality_report(df_raw, dedup_col=config.dedup_col)
    df_text, df_time = preprocess_reviews(df_raw, config=config)

    summary_stats = build_summary_statistics(df_text)
    daily_trend = build_daily_trend(df_time)
    image_compare = build_image_comparison(df_text)

    save_processed_reviews(df_text, df_time, output_dir="data/processed")

    output_table_dir = Path("outputs/tables")
    output_table_dir.mkdir(parents=True, exist_ok=True)

    quality_report.to_csv(output_table_dir / "quality_report.csv", index=False, encoding="utf-8-sig")
    summary_stats.to_csv(output_table_dir / "summary_statistics.csv", index=False, encoding="utf-8-sig")
    daily_trend.to_csv(output_table_dir / "daily_trend.csv", index=False, encoding="utf-8-sig")
    image_compare.to_csv(output_table_dir / "image_comparison.csv", index=False, encoding="utf-8-sig")

    print("=" * 60)
    print("[품질 점검]")
    print(quality_report)
    print("\n[기초 통계]")
    print(summary_stats)
    print("\n[일별 추이 상위 5개]")
    print(daily_trend.head())
    print("\n[이미지 포함 여부 비교]")
    print(image_compare)
    print("=" * 60)