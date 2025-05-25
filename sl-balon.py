import streamlit as st

st.title("Balonlar")

if st.button("Balon Gönder", icon="🎈", use_container_width=True):
	st.balloons()
