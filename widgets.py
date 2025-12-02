

st.title("1. Basic Widgets Demo")

st.header("Buttons & text inputs")
name = st.text_input("what is your name?")
if st.button("Say hello"):
    if name: 
        st.success(F"Hello, {name}")
    else: 
        st.warning("Please enter your name first.")

st.divider()

st.header("Numeric inputs")

age= st.number_input("Your age", min_value=0, max_value=120, value= 25)
st.write("You entered age:", age)

st.slider("Pick a value", min_value=0, max_value=120, value=50, key= "slider_example")

st.divider() 

st.header("Selection widgets")
color= st.selectbox("Favourite color",["Red", "Green", "Blue"])
options= st.multiselect("Choose some fruits", ["Apple", "Banana", "Orange", "Grapes"])
st.write("Color:", color)
st.write("fruits:", options)

st.divider()

st.header("Booleans and Dates")
agree= st.checkbox("I agree to the terms")
if agree: 
    st.info("Thanks for agreeing")

date= st.date_input("Pick a date")
st.write("Chosen date:", date)