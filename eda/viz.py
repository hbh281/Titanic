import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font_path = r"font/NanumGothic-Regular.ttf"  # hoặc đường dẫn tuyệt đối
fm.fontManager.addfont(font_path)  # ✅ Bắt buộc để matplotlib biết font này

font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()  # đúng tên trong file .ttf
plt.rcParams['axes.unicode_minus'] = False

def survivorsChart(df):
    st.markdown("## 1.성별별 생존율 \n")
    st.markdown("<hr>", unsafe_allow_html=True)
    col1,col2 =st.columns(2)
    with col1:
        st.subheader("성별별 총 승객수")
        fig_passenger= px.pie(
            df,
            names ="Sex",
            color="Sex",
            title="총 승객수: 남성 vs 여성:",
            labels={"Sex": "성별","value":"승객수"},
            color_discrete_map={"male": "#75c4fd", "female": "#fec6e2"},
        )
        fig_passenger.update_traces(
            textinfo='percent+value',
            pull=[0.03]
        )
        st.plotly_chart(fig_passenger, use_container_width=True)

    with col2:
        st.subheader("성별별 생존 승객수")
        survivors = df[df["Survived"]== 1]
        fig_passenger = px.pie(
            survivors,
            names="Sex",
            color="Sex",
            title = "총 생존 승객수: 남성 vs 여성:",
            labels = {"Sex": "성별", "value":"승객수"},
            color_discrete_map={"male": "#75c4fd", "female": "#fec6e2"},
        )
        fig_passenger.update_traces(
            textinfo='percent+value',
            pull=[0.03])
        st.plotly_chart(fig_passenger,use_container_width=True)
        
    
    st.markdown("## 2.클래스별 생존율 \n")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    surv_by_pclass = (
    df.groupby('Pclass')['Survived']
      .mean()
      .reset_index(name='survival_rate')
    )
    surv_by_pclass['Pclass'] = surv_by_pclass['Pclass'].astype(str) #chuyen thanh str de in khong bi 1.5,2.5
    fig1 = px.bar(
        surv_by_pclass,
        x='Pclass', y='survival_rate',
        labels={'class':'Pclass', 'survival_rate':'생존율'},
        color= 'Pclass',
        color_discrete_map= {"1" : "#F8E57C", "2" : "#D4D4D4", "3" : "#FFAC5A"},
        title="클래스별 생존율"
    )
    fig1.update_layout(xaxis_type='category') #ep kieu de truc x la kieu category(khong phai so)
    
    st.plotly_chart(fig1, use_container_width=True)
    
    
    st.markdown("## 3.운임별 생존율 \n")
    st.markdown("<hr>", unsafe_allow_html=True)
    
    
    fig = px.histogram(df, x="Survived", color="Sex",color_discrete_map= {"male": "#75c4fd", "female" : "#fec6e2"}, facet_col="Embarked")
    st.plotly_chart(fig)

    # fig = px.bar(
    # surv_by_pclass,
    # x='Pclass',
    # y='survival_rate',
    # facet_col='Sex',
    # color='Sex',
    # labels={'Pclass': '등급', 'survival_rate': '생존율'},
    # title="클래스 × 성별 생존율 (Facet)"
    # )
    # fig.update_layout(xaxis_type='category')
    # st.plotly_chart(fig)
    
    
def Age(df):
    st.markdown("## 1.성별별 나이 분포 \n")
    st.markdown("<hr>", unsafe_allow_html=True)
    fig,ax = plt.subplots(figsize =(10,6))
    sns.histplot(data=df, x = 'Age',kde = True, hue = 'Sex',ax = ax)
    ax.set_title('나이 분포')
    st.pyplot(fig)
    
    
    
    st.markdown("## 2.성별 및 생존여부에 따른 나이 분포 \n")
    st.markdown("<hr>", unsafe_allow_html=True)
    df['Survived_label'] = df['Survived'].map({0: '사망', 1: '생존'})


    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(
        x="Sex",
        y="Age",
        hue="Survived_label",  
        data=df,
        split=True,
        palette={"생존": "#2ecc71", "사망": "#e74c3c"},
        ax =ax
    )
    plt.title("성별 및 생존여부에 따른 나이 분포")
    st.pyplot(fig)

    
    st.markdown("## 3.생존과 관련된 티켓 가격 \n")
    st.markdown("<hr>", unsafe_allow_html=True)

    fig_fare_box = px.box(
        df,
        x='Pclass',
        y='Fare',
        color='Survived_label',  
        title="등급 및 생존여부에 따른 운임 분포 (Boxplot)",
        labels={'Fare': '운임 (Fare)', 'Pclass': '등급'},
        color_discrete_map={'생존': '#2ecc71', '사망': '#e74c3c'}
    )
    st.plotly_chart(fig_fare_box, use_container_width=True)

def relation_matrix(df):
    
    st.markdown("## 📊 상관 행렬 분석")
    st.markdown("수치형 변수 간의 관계를 시각적으로 확인할 수 있습니다.")

    corr = df.select_dtypes(include='number').corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", ax=ax)
    ax.set_title("수치형 변수 간 상관 행렬")
    st.pyplot(fig)
    
def showViz(df):
    selected = st.sidebar.selectbox(
        "차트 메뉴 선택",
        ["그룹별 생존율", "연령 및 운임 분포", "상관 행렬"]
    )
    if selected == "그룹별 생존율":
        survivorsChart(df)
    elif selected == "연령 및 운임 분포":
        Age(df)
    elif selected == "상관 행렬":
        relation_matrix(df)
        
    
