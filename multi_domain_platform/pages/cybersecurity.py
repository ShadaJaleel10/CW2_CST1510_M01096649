import streamlit as st
from services.database_manager import DatabaseManager 
from models.security_incident import SecurityIncident 

st.title("Cybersecurity Domain")

if 'db' not in st.session_state:
    st.session_state['db']= DatabaseManager("database/platform.db")

db: DatabaseManager= st.session_state['db']
db.connect() 

#Replace direct SQL with DatabaseManager
rows = db.fetch_all(
    "SELECT id, incident_type, severity, status, description FROM security_incidents"
) 

incidents: list[SecurityIncident] = [] 

for row in rows:
    incident= SecurityIncident(
        incident_id=row[0], 
        incident_type=row[1], 
        severity=row[2], 
        status=row[3],
        description=row[4], 
    )
    incidents.append(incident) 

st.subheader("Security Incidents Overview")
for incident in incidents:
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.metric(label=f"Incident ID {incident.get_id()}", value=incident.get_severity_level()) 
    
    with col2:
        st.write(f"**Type:** {incident._incident_type}")
        st.write(f"**Status:** {incident._status}")
        st.caption(incident.get_description()[:100] + "...")

    with col3:
        # Eg. using object method to prepare data for AI
        ai_prompt= f"Summarize the severity for this incident: {incident.get_description()}"
        if st.button("Analyze with AI", key=f"ai_{incident.get_id()}"):
            st.info("AI Analysis Placeholder")