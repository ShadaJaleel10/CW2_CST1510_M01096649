import streamlit as st
from services.database_manager import DatabaseManager 
from services.auth_manager import AuthManager 

#Initialization
if 'db' not in st.session_state:
    st.session_state['db']= DatabaseManager("database/platform.db") 
    st.session_state['auth']= AuthManager(st.session_state['db'])

#login logic
st.title("User Login")

username= st.text_input("Username") 
password= st.text_input("Password", type="password") 

if st.button("Login"):
    user= st.session_state['auth'].login_user(username, password) 

    if user is None:
        st.error("Login failed. Invalid username or password.") 
    else:
        st.success(f"Login successful for: {user}") 
        st.session_state["current_user"] = user.get_username()
        st.session_state["current_role"] = user.get_role() 
        st.rerun()

 