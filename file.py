import streamlit as st 
import pandas as pd 

df= pd.DataFrame ({
"year": [2023, 2024, 2025],
"revenue": [25000, 32000, 29000]
})

st.set_page_config(layout= "wide")
st.title("Sales Dashboard")

with st.sidebar: 
    year= st.selectbox("Year", [2023,2024,2025])
    min_revenue= st.slider(
        "Min revenue", 0, 100000, 20000
)

filtered= df[(df["year"] == year) & 
             (df["revenue"] >= min_revenue)]

col1,col2 = st.columns(2) 

with col1: 
    st.subheader("Revenue by Region")
    st.bar_chart(filtered)

with col2: 
    st.subheader("Revenue Distribution")
    st.line_chart(filtered)

with st.expander("See filtered data"): 
    st.dataframe(filtered)