import streamlit as st
from services.database_manager import DatabaseManager
from models.it_ticket import ITTicket #

st.title("IT Operations Domain")

if 'db' not in st.session_state:
    st.session_state['db'] = DatabaseManager("database/platform.db")

db: DatabaseManager = st.session_state['db']
db.connect()

#eg. SQL
rows = db.fetch_all(
    "SELECT ticket_id, title, priority, status, assigned_to FROM it_tickets"
)

tickets: list[ITTicket] = []

for row in rows:
    ticket = ITTicket(
        ticket_id=row[0],
        title=row[1],
        priority=row[2],
        status=row[3],
        assigned_to=row[4],
    )
    tickets.append(ticket)

st.subheader(f"Open IT Tickets ({len([t for t in tickets if t.get_status() != 'Closed'])})")

for ticket in tickets:
    if ticket.get_status() != "Closed":
        col1, col2, col3 = st.columns([1, 2, 2])

        with col1:
            st.metric(label="Priority", value=ticket._priority)
        
        with col2:
            st.write(f"**ID:** {ticket._id}")
            st.write(f"**Title:** {ticket._title}")
        
        with col3:
            st.write(f"**Status:** {ticket.get_status()}")
            st.write(f"**Assigned To:** {ticket._assigned_to}")
            
            if st.button("Close Ticket", key=f"close_{ticket._id}"):
                ticket.close_ticket() 
                st.session_state['db'].execute_query(
                    "UPDATE it_tickets SET status = 'Closed' WHERE ticket_id = ?",
                    (ticket._id,)
                )
                st.success(f"Ticket {ticket._id} closed!")
                st.rerun()

