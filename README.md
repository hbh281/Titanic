# Titanic
Titanic dataset visualization
# 🚢 Titanic 생존자 예측 대시보드

이 프로젝트는 Titanic 탑승객 데이터를 기반으로 생존 여부를 분석하고, 시각화하며, 머신러닝 모델을 활용하여 특정 인물(Jack & Rose)의 생존 확률을 예측하는 대시보드입니다.  

![preview](./data/featured.jpg)

---

## 📌 주요 기능

### 1. 홈 (Home)
- 프로젝트 소개
- 전체 승객 수 및 통계 요약
- 데이터 미리보기

### 2. 탐색적 자료 분석 (EDA)
- **성별 및 클래스별 생존율 시각화**
- **나이 및 요금 분포 분석**
- **상관관계 분석 (Correlation Matrix)**
- **성별·생존여부에 따른 Violin Plot**
- **Embarked 항구별 생존 차이 시각화**

### 3. 예측 (Prediction)
- `RandomForestClassifier`를 활용하여 Jack & Rose의 생존 확률 예측
- 결과를 **막대 그래프**, **도넛 차트**, **게이지 차트**로 시각화
- 모델의 예측 이유에 대한 설명 포함
## 🧠 사용한 기술 스택

| 분야 | 기술 |
|------|------|
| 프론트엔드 | Streamlit |
| 시각화 | Plotly, Seaborn, Matplotlib |
| 데이터 처리 | Pandas, NumPy |
| 머신러닝 | Scikit-learn |
| 기타 | Millify, streamlit-option-menu |

---

## 📂 폴더 구조

Titanic/
├── app.py                # 메인 앱 실행 파일
├── utils.py              # 데이터 로드 및 전처리 함수
├── preprocessing.py      # 전처리 함수
├── prediction.py         # 예측 관련 함수
├── home.py               # 홈 화면 구성
├── eda/
│   ├── eda_home.py       # EDA 진입점
│   └── viz.py            #  시각화 함수
├── data/
│   ├── train.csv         # Titanic dataset (from Kaggle)
│   └── featured.jpg
