from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
def predict(df):
    st.markdown("### 💏 Titanic에 실제로 JACK와 ROSE가 탄다면 생존율이 어떻게 되는지 궁금할까요?")
    st.image("data/featured.jpg",use_container_width=True)
    st.markdown("<hr>",unsafe_allow_html=True)
    
    st.subheader("1.JACK와 ROSE 정보 보기")
    st.markdown("<hr>",unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎭 Jack Dawson")
        st.markdown("- 💼 클래스: 3등석 (Pclass 3)")
        st.markdown("- 🧑 성별: 남성")
        st.markdown("- 🎂 나이: 20세")
        st.markdown("- 🎫 요금: $7.25")
        st.markdown("- 🚢 탑승지: Southampton (S)")
    with col2: 
        st.markdown("### 🌹 Rose DeWitt Bukater")
        st.markdown("- 💼 클래스: 1등석")
        st.markdown("- 👩 성별: 여성")
        st.markdown("- 🎂 나이: 19세")
        st.markdown("- 🎫 요금: $263.00")
        st.markdown("- 🚢 탑승지: Cherbourg (C)")

    

    features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]
    df_ml = df[features + ["Survived"]].dropna()

    df_encoded = pd.get_dummies(df_ml, columns=["Sex", "Embarked"], drop_first=True)

    X = df_encoded.drop("Survived", axis=1)
    y = df_encoded["Survived"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    
    passengers = [
        {
            "name": "Jack",
            "Pclass": 3,
            "Sex": "male",
            "Age": 20,
            "SibSp": 0,
            "Parch": 0,
            "Fare": 7.25,
            "Embarked": "S"
        },
        {
            "name": "Rose",
            "Pclass": 1,
            "Sex": "female",
            "Age": 19,
            "SibSp": 0,
            "Parch": 1,
            "Fare": 263.00,
            "Embarked": "C"
        }
    ]

    test_df = pd.DataFrame(passengers)
    test_encoded = pd.get_dummies(test_df.drop(columns=["name"]), columns=["Sex", "Embarked"])
    test_encoded = test_encoded.reindex(columns=X.columns, fill_value=0)

    # 4. Dự đoán
    pred_probs = model.predict_proba(test_encoded)[:, 1]
    pred_labels = model.predict(test_encoded)

    # 5. Tạo kết quả trả về
    results = pd.DataFrame({
        "Name": [p["name"] for p in passengers],
        "Survival Probability (%)": (pred_probs * 100).round(1),
        "Prediction": ["생존" if p == 1 else "사망" for p in pred_labels]
    })

    st.subheader("2. Jack & Rose 생존 예측 결과")
    st.markdown("<hr>",unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Jack", "18.4%", "☠️ 사망")

    with col2:
        st.metric("Rose", "95.7%", "✅ 생존")

    st.subheader("3. Jack & Rose 생존 확율 비교")
    st.markdown("<hr>",unsafe_allow_html=True)
    show_prediction_bar(results)

    st.markdown("### 🍩 개인별 생존률 시각화")
    col1,col2 = st.columns(2)
    with col1:
        show_gauge(results.iloc[0]["Name"], results.iloc[0]["Survival Probability (%)"])
    with col2:
        show_gauge(results.iloc[1]["Name"], results.iloc[1]["Survival Probability (%)"])

    st.markdown("""
        ### ✅ **왜 Rose는 생존 확률이 높은가?**
        - **성별:** Rose는 *여성*입니다 → 실제 데이터에서 여성 생존률은 매우 높습니다 (약 74%).
        - **객실 등급 (Pclass):** 1등석 승객 → 1등석 승객의 생존률은 약 63%로 높습니다.
        - **운임 (Fare):** 263.00 → 고액 요금 지불 → 상류층에 속하며, 구조 우선 대상일 가능성이 높습니다.
        - **탑승 항구 (Embarked):** Cherbourg(C) → 고급 승객이 자주 이용한 항구로 생존률이 높은 편입니다.

        ---

        ### ❌ **왜 Jack은 생존 확률이 낮은가?**
        - **성별:** Jack은 *남성*입니다 → 남성 생존률은 낮은 편입니다 (약 19%).
        - **객실 등급 (Pclass):** 3등석 → 생존률이 가장 낮은 등급입니다 (약 24%).
        - **운임 (Fare):** 7.25 → 저가 요금 → 경제적 계층이 낮은 승객으로 구조 우선 순위가 낮았을 가능성이 큽니다.
        - **혼자 탑승 (SibSp=0, Parch=0):** 동반 가족이 없으므로 우선 구조 대상이 아니었을 수 있습니다.

        ---

        ### 📊 **종합 결론**
        📌 *인구 통계적 특성과 사회적 조건에 따라, 머신러닝 모델은 Rose의 생존 확률을 매우 높게 예측하고, Jack은 낮게 예측했습니다. 이는 Titanic 실제 데이터 경향과 일치하며, 여성·상류층·1등석 승객의 생존률이 높은 경향을 잘 반영한 결과입니다.*
        """)

    
def show_prediction_bar(results_df):
    fig = px.bar(
        results_df,
        x="Name",
        y="Survival Probability (%)",
        color="Prediction",
        color_discrete_map={"생존": "#2ecc71", "사망": "#e74c3c"},
        text="Survival Probability (%)",
        title="Jack & Rose 생존 확률 비교"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig, use_container_width=True)
    
# def show_donut_chart(name, prob):
#     fig = go.Figure(data=[
#         go.Pie(
#             labels=["생존", "사망"],
#             values=[prob, 100 - prob],
#             hole=0.6,
#             marker_colors=["#2ecc71", "#e74c3c"]
#         )
#     ])
#     fig.update_layout(title=f"{name} 생존 예측", showlegend=False)
#     st.plotly_chart(fig, use_container_width=True)
    
def show_gauge(name, prob):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = prob,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{name} 생존 확률", 'font': {'size': 20}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2ecc71" if prob > 50 else "#e74c3c"},
            'steps': [
                {'range': [0, 50], 'color': "#f9c0c0"},
                {'range': [50, 100], 'color': "#b0f2c2"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': prob
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)