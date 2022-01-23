import streamlit as st
import pandas as pd
import numpy as np
from CovidPage.covid import make_covid_dashboard


st.set_page_config(layout="wide")


def side_bar():

    sidebar = st.sidebar

    sidebar.title("Menu")

    global add_selectbox
    add_selectbox = sidebar.selectbox(
        "Project Selection", ("COVID Dashboard", "Location Breakdown")
    )

    sidebar.title("Welcome!!")
    sidebar.info(
        """
        Hello! My name is Brendan and I'm an avid data analyst & analytics engineer with a **HUGE** heart for data!!
        The below tabs represent my current portfolio of data apps, that I'm always looking for feedback on!!

        Feel free to drop a note below with any critiques or recommendations to make them better 🙂
        """
    )

    sidebar.title("Feedback")
    form = sidebar.form("my form")
    subject = form.text_input("Subject")
    body = form.text_input("Feedback")
    submitted = form.form_submit_button("Submit")

    if submitted:
        form.write("submitted")


def current_page():

    st.markdown(
        f"<h1 style='text-align: center;'>{add_selectbox}</h1>", unsafe_allow_html=True,
    )
    if add_selectbox == "COVID Dashboard":
        make_covid_dashboard()


def main():
    side_bar()
    current_page()


if __name__ == "__main__":
    main()
