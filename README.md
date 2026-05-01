# CGV Movie Review Analytics with Sentiment Analysis & BERTopic

> CGV 영화 리뷰 데이터를 기반으로 관객 반응의 감성 분포, 시계열 변화, 핵심 표현 구조, 그리고 BERTopic 기반 토픽 구조를 분석한 Streamlit 프로젝트입니다.  
> 영화 소비자 반응을 데이터 기반으로 해석하고, 이를 시각적으로 전달하는 포트폴리오형 텍스트 분석 프로젝트입니다.

<br>

## 📌 Project Overview

- **Project Name**: CGV Movie Review Analytics
- **Repository**: `cgv-review-pilot-analysis`
- **Analysis Target**: CGV audience reviews for the movie `<왕과 사는 남자>`
- **Final Clean Data**: 49,010 reviews
- **Review Period**: 2026-02-05 ~ 2026-03-29
- **Positive Review Ratio**: 97.07%
- **Main Methods**
  - Text preprocessing
  - Sentiment analysis
  - Time-series review trend analysis
  - Keyword analysis
  - BERTopic topic modeling
  - Streamlit dashboard implementation
- **Streamlit App**: https://cgv-review-pilot-analysis.streamlit.app

---

## 📖 프로젝트 개요

온라인 영화 리뷰는 단순한 감상문을 넘어,  
관객의 기대, 만족, 몰입, 실망, 비교 평가가 집약된 디지털 텍스트 데이터입니다.

본 프로젝트는 CGV 영화 리뷰 데이터를 수집·정제한 뒤,  
감성 분석과 BERTopic 토픽 모델링을 활용하여 관객 반응의 구조를 분석했습니다.

핵심 질문은 다음과 같습니다.

- 관객 반응은 전체적으로 얼마나 긍정적인가?
- 반응은 시간에 따라 어떻게 변화하는가?
- 긍정 리뷰와 부정 리뷰는 각각 어떤 표현을 중심으로 형성되는가?
- 관객 반응은 어떤 토픽 구조로 나뉘는가?
- 온라인 플랫폼 리뷰 데이터는 영화 소비자 반응을 어떻게 보여주는가?

본 프로젝트는 단순 평점 확인을 넘어,  
**디지털 플랫폼 위에서 형성되는 집단적 관객 반응 구조**를 데이터로 읽어보려는 시도입니다.

---

## 🎯 Project Goals

### 1. 대규모 리뷰 데이터 분석

- CGV 영화 리뷰 49,010건 기반 분석
- 실제 사용자 생성 텍스트 데이터 활용
- 리뷰 작성 기간: 2026-02-05 ~ 2026-03-29

### 2. 관객 반응 정량화

- 전체 감성 분포 확인
- 긍정·부정 리뷰 비율 비교
- 날짜별 리뷰 수와 긍정 비율 추이 분석
- 초반·중반·후반 시기별 반응 비교

### 3. 담론 구조 해석

- 긍정 리뷰 핵심 표현 분석
- 부정 리뷰 핵심 표현 분석
- 결합 표현 및 TF-IDF 기반 주요 표현 확인
- BERTopic 기반 주요 토픽 구조 도출

### 4. Streamlit 기반 시각화

- 분석 결과를 비개발자도 이해할 수 있는 형태로 구성
- 프로젝트 소개 페이지와 분석 결과 페이지 분리
- 포트폴리오 제출용 대시보드 구현

---

## 📊 Key Findings

### 1. Sentiment Distribution

최종 clean 데이터 49,010건 기준으로,  
전체 리뷰 중 긍정 리뷰 비율은 **97.07%** 로 나타났습니다.

이는 영화 `<왕과 사는 남자>`에 대한 관객 반응이  
전반적으로 매우 긍정적인 방향으로 형성되었음을 보여줍니다.

---

### 2. Positive Review Structure

긍정 리뷰에서는 다음과 같은 표현 축이 두드러졌습니다.

- 배우 연기
- 감동
- 여운
- 몰입감
- 만족스러운 관람 경험
- 한국영화에 대한 긍정적 평가

긍정 반응은 단순히 “재미있다”는 평가를 넘어,  
배우의 연기력과 영화가 제공한 감정적 경험을 중심으로 형성되었습니다.

---

### 3. Negative Review Structure

전체적으로 긍정 비율이 압도적으로 높았지만,  
부정 리뷰에서는 다음과 같은 표현이 상대적으로 두드러졌습니다.

- 스토리
- 연출
- 기대 대비 아쉬움
- CG
- 개연성
- 지루함

즉, 부정 반응은 작품 전체에 대한 전면적 부정보다는  
특정 요소에 대한 세부적 아쉬움으로 나타났습니다.

---

## 🧠 BERTopic Topic Modeling

BERTopic 분석 결과, 관객 반응은 다음 4개 주요 토픽으로 정리되었습니다.

| Topic | Interpretation |
|------|----------------|
| Topic 0 | 배우 연기와 감동 중심의 전반적 호평 |
| Topic 1 | 유해진·박지훈 연기에 대한 집중 호평 |
| Topic 2 | 오랜만에 만족스러운 한국영화라는 반응 |
| Topic 3 | 호랑이 CG에 대한 아쉬움 |

BERTopic 결과는 관객 반응이 단순한 긍정·부정 이분법이 아니라,  
**배우 연기, 감동, 한국영화에 대한 만족감, CG 아쉬움** 등  
여러 담론 축으로 구성되어 있음을 보여줍니다.

---

## 🧩 Interpretation Framework

### 1. 기대불일치 이론

관객은 영화 관람 전에 이미 기대를 형성합니다.  
실제 경험이 기대를 충족하거나 초과하면 긍정 평가가 강화되고,  
기대에 미치지 못하면 구체적 아쉬움이 리뷰에 나타날 수 있습니다.

본 프로젝트에서 확인된 일부 부정 표현은  
작품 전체에 대한 부정보다는 **기대 대비 아쉬움**으로 해석할 수 있습니다.

---

### 2. 사회적 증거 / 밴드왜건 효과

높은 화제성, 추천, 입소문은 후기 관객의 기대 수준을 높일 수 있습니다.  
따라서 리뷰 평가는 영화 자체뿐 아니라  
사회적으로 형성된 기대의 영향도 받을 수 있습니다.

---

### 3. 플랫폼 리뷰 데이터의 방법론적 의미

온라인 리뷰는 관객이 자발적으로 남긴 대규모 텍스트 데이터입니다.  
설문조사와 달리 관람 직후의 표현, 감정, 평가 기준을 실시간에 가깝게 포착할 수 있습니다.

따라서 본 프로젝트는 플랫폼 리뷰 데이터를 활용해  
소비자 반응과 담론 구조를 분석한 사례로 볼 수 있습니다.

---

## 🖥️ Streamlit Dashboard

Streamlit 앱은 다음과 같은 구조로 구성했습니다.

### 1. Main Page

- 프로젝트 개요
- 분석 기간
- 분석 리뷰 수
- 긍정·부정 비율
- 핵심 분석 결과
- 연구 질문
- BERTopic 주요 토픽 구조
- 이론적 해석 가능성
- 분석 결과 페이지 이동 버튼

### 2. Analysis Page

- 핵심 요약
- 날짜별 긍정 비율 추이
- 날짜별 리뷰 수 변화
- 초반·중반·후반 비교
- 긍정 리뷰 핵심 표현
- 부정 리뷰 핵심 표현
- 결합 표현 분석
- TF-IDF 주요 표현
- BERTopic 토픽 요약
- 대표 리뷰 예시
- 종합 해석

---

## 🗂 Project Structure

```text
cgv-review-pilot-analysis/
├─ README.md
├─ requirements.txt
│
├─ app/
│  ├─ streamlit_app.py
│  ├─ pages/
│  │  └─ 01_분석결과.py
│  └─ assets/
│     └─ images/
│        └─ movie_poster.jpg
│
├─ data/
│  └─ processed/
│
├─ notebooks/
│
├─ outputs/
│  ├─ figures/
│  └─ tables/
│
└─ src/
   ├─ preprocessing/
   ├─ analysis/
   └─ utils/
```

---

## 🛠 Tech Stack

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Matplotlib-0A84FF?style=for-the-badge" alt="Matplotlib">
  <img src="https://img.shields.io/badge/BERTopic-111827?style=for-the-badge" alt="BERTopic">
  <img src="https://img.shields.io/badge/Jupyter-6B7280?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
  <img src="https://img.shields.io/badge/GitHub-24292F?style=for-the-badge&logo=github&logoColor=white" alt="GitHub">
</p>

---

## 📌 Project Significance

본 프로젝트는 다음의 흐름을 하나로 연결한 실전형 데이터 분석 프로젝트입니다.

1. 대규모 리뷰 데이터 수집
2. 텍스트 전처리
3. 감성 분석
4. 키워드 및 결합 표현 분석
5. BERTopic 기반 토픽 모델링
6. Streamlit 기반 결과 시각화
7. 관객 반응에 대한 해석

즉, 단순히 모델을 적용하는 데 그치지 않고,  
**데이터 분석 → 해석 → 시각화 → 전달**까지 연결했다는 점에 의미가 있습니다.

---

## 👤 Author

**Ji-Eun Son**
