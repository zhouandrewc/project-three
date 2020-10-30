#
# Streamlit app for bachelor's degree predictor
# Andrew Zhou
#
# Some code taken from demos from https://github.com/streamlit/
#

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sys

sys.path.append("..")

from util.modeling import prepro
from streamlit.report_thread import get_report_ctx
import streamlit.components.v1 as components


st.beta_set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def init(user_session_id):
    return {"run_next": 0}

ctx = get_report_ctx()
status = init(ctx.session_id)

st.markdown('<style>.stButton { text-align: center; } iframe { text-align: center; } </style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center';>Predicting Future College Graduation from Childhood Data</h1>", unsafe_allow_html=True)
st.text("")

col_1, _, col_2, _, col_3 = st.beta_columns((1, 0.1, 1, 0.1, 1))

with col_1:
    button_1 = st.button("Graduation Prediction")
with col_2:
    button_2 = st.button("Feature Exploration")
with col_3:
    button_3 = st.button("Model Performance")
if button_1:
    status["run_next"] = 1
elif button_2:
    status["run_next"] = 2
elif button_3:
    status["run_next"] = 3


if status["run_next"] == 0:
    col2_1, _, col2_2, _, col3_3 = st.beta_columns((1, 0.1, 1, 0.1, 1))
    st.write("")
    st.write("")
    with col2_2:
        st.markdown("<h1 style='text-align: center;'>Welcome! Please choose a page!</h1>", unsafe_allow_html=True)
if status["run_next"] == 1:
    # LAYING OUT THE TOP SECTION OF THE APP
    col3_1, _, col3_2, _, col3_3 = st.beta_columns((1.3, 0.2, 1.3, 0.2, 1.3))

    with col3_1:
        st.markdown("**Family Status (2001)**")
        wealth = st.slider("Wealth", 0, 250000, value=50000)
        income = st.slider("Income", 0, 250000, value=50000)
        environ = st.selectbox("Living Environment", ("Large Metro", "Small Metro", "Metro City", "Non-Metro City", "Metro Fringe", "Rural"))
        food_security = st.selectbox("Food Security", ("High", "Marginal", "Low", "Very Low"))
        parents = st.selectbox("Lives With:", ("Two Parents", "One or No Parents"))

    with col3_2:
        st.markdown("**Test Scores**")
        math = st.slider("Math Percentile", 0, 100, value=50, step=1)
        reading = st.slider("Reading Percentile", 0, 100, value=50, step=1)

    with col3_2:
        st.markdown("**Demographics**")
        age = st.slider("Age", 22, 35, value=28)

    with open("models/rf_best.pickle", "rb") as model_pickle:
        rf_best = pickle.load(model_pickle)

    def get_env():
        if environ == "Large Metro":
            return "met_central"
        if environ == "Metro Fringe":
            return "met_fringe"
        if environ == "Small Metro":
            return "met_small"
        if environ == "Metro City":
            return "urb_met"
        if environ == "Non-Metro City":
            return "urb_nonmet"
        if environ == "Rural":
            return "rural"

    def check_race(to_check):
        return 1 if to_check == race else 0

    def get_parents():
        return 1 if parents == "Two Parents" else 0

    def get_food_security():
        if food_security == "High":
            return 0
        elif food_security == "Marginal":
            return 1.5
        elif food_security == "Low":
            return 4
        else:
            return 8


    X = pd.DataFrame([[math, reading, wealth, income, get_env(), age,\
                     0, 0, 0,\
                      get_parents(), get_food_security(), 0]],\
                      columns=["math", "reading", "wealth", "income", "environment_type",\
                      "age", "white_only", "black", "asian", "live_w_both_parents",
                      "food_security", "hispanic"])

    X_train = pd.read_csv("train_data.csv")

    X_tr_prepro, X_prepro = prepro(X_train, X)

    prediction = rf_best.predict(X_prepro)

    with col3_3:
        st.markdown("<h3 style='text-align: center; color: black;'>We predict that this student has a</h3>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: red;'>" + str(int(rf_best.predict_proba(X_prepro)[0][1]*100.0)) + "%</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center'; color: black;'>chance of receiving a bachelor's degree.</p>", unsafe_allow_html=True)
elif status["run_next"] == 2:
    st.markdown("<h3 style='text-align: center;'>Click a feature on the left chart to show its relationship with graduation on the right.</h3>", unsafe_allow_html=True)
    col4_1, col4_2 = st.beta_columns((0.25, 2))

    # Show flask app in iframe. Location will depend on where it's being hosted
    with col4_2:
        bar_loc = "http://127.0.0.1:5000/bar"
        components.iframe(bar_loc, width= 1800, height=1500, scrolling=False)
elif status["run_next"] == 3:
    st.write("Under Construction")




