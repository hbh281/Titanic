# -*- coding:utf-8 -*-
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from eda.viz import showViz
from millify import prettify 
from utils import load_data
from eda.map import showEmbarkedMap

def home():
    total_df = load_data()
    survivors = prettify(total_df['Survived'].value_counts()[1])
    deads = prettify(total_df['Survived'].value_counts()[0])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #e0f7fa'>
                <div style='font-size: 24px; font-weight: bold;'>🎉생존자 수</div>
                <div style='font-size: 36px; color: green;'>{survivors}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style='text-align: center; padding: 20px; border-radius: 10px; background-color: #ffebee'>
                <div style='font-size: 24px; font-weight: bold;'>☠️사망자 수</div>
                <div style='font-size: 36px; color: red;'>{deads}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "### 1.🖼️ Visualization 개요 \n"
        "- 그룹별 생존율. \n"
        "- 연령 및 운임 분포. \n"
        "- 상관 행렬. \n"
        "- Embarked 분석."
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        "### 2.🗺️ Map 개요 \n"
        "- 이 지도는 타이타닉 탑승객들이 출발한 항구(C, Q, S)의 위치를 시각화하여, 각 항구에서 출발한 승객 수를 비교하고자 한다.\n"
        "각 항구의 위도(lat), 경도(lon)는 수동으로 매핑하였으며, 승객의 Embarked 컬럼을 통해 항구별로 분류하였다."
    )


def run_eda(total_df):
    # total_df["DEAL_YMD"] = pd.to_datetime(total_df["DEAL_YMD"], format="%Y-%m-%d")
    
    st.markdown(
        "## 탐색적 자료 분석 개요 \n"
        "탐색적 자료분석 페이지입니다. "
        "여기서 Titanic 데이터세트에 대해 분석 및 시각화 페이지입니다. 👇👇👇"
    )
    selected = option_menu(
        None,
        ["Home", "Visualization", "Map"],
        icons=["house", "bar-chart",  "map"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#fafafa",
            },  # fafafa #6F92F7
            "icon": {"color": "orange", "font-size": "25px"},
            "nav-link": {
                "font-size": "18px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#eee",
            },
            "nav-link-selected": {"background-color": "green"},
        },
    )

    if selected == "Home":
        home()
    elif selected == "Visualization":
        # st.title("Visualization")
        showViz(total_df)
    elif selected == "Map":
        showEmbarkedMap(total_df)
    else:
        st.warning("Wrong")
