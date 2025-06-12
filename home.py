import pandas as pd 
from utils import load_data
import streamlit as st 
from millify import prettify 

def run_home():
    total_df = load_data()
    if total_df is None:
        st.error("🚨 데이터 로딩 실패! Titanic 데이터를 불러올 수 없습니다.")
        return
    st.write("## 📋대시보드 개요\n")
    st.markdown(
    
        "본 프로젝트는 Titanic 승객에 대한 정보를 알려주는 대시보드입니다.\n"
        "\n이 데이터세트를 분석을 통해 어떤 사람이 생존할 것 같느냐 예측하는 것입니다."
    )
    
    st.image("data/titanic.png",use_container_width=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader(f"⛴️총 승객 수:")
    total_passengers = prettify(total_df.shape[0]) 
    st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color:#333;'>""" + total_passengers + "명""""</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("📈 데이터 통계")
    st.dataframe(total_df.describe())
    
    
