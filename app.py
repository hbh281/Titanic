import streamlit as st 
from streamlit_option_menu import option_menu
from home import run_home
from utils import load_data
from eda.predict import predict
from eda.eda_home import run_eda

def main():
    with st.sidebar:
        total_df = load_data()
        selected = option_menu(
            "Dashboard menu",
            ["홈","탐색적 자료 분석","생존율 예측"],
            icons = ["house","file-bar-graph","graph-up-arrow"],
            menu_icon = "cast",
            default_index = 0,
        )
    if selected == "홈":
        run_home()

    elif selected == "탐색적 자료 분석":
        run_eda(total_df)
    elif selected == "생존율 예측":
        predict(total_df)
    else: 
        print("error.....")

if __name__ == "__main__":
    main()