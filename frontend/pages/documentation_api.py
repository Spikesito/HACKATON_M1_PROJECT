import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.header("🗂️ Documentation API", divider="orange")

components.iframe("http://localhost:8000/docs", height=600, scrolling=True)