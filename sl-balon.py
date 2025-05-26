import streamlit as st
from camelcase import CamelCase

c = CamelCase()
title = "balon uçurma uygulaması"

st.title(c.hump(title))

if st.button("Balon Gönder", icon="🎈", use_container_width=True):
	st.balloons()
