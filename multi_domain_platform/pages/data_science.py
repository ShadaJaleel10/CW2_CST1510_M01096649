import streamlit as st
from services.database_manager import DatabaseManager
from models.dataset import Dataset #

st.title("Data Science Domain")

if 'db' not in st.session_state:
    st.session_state['db']= DatabaseManager("database/platform.db")

db: DatabaseManager= st.session_state['db']
db.connect()

#eg. SQL
rows = db.fetch_all(
    "SELECT dataset_id, name, size_bytes, rows, source FROM datasets"
)

datasets: list[Dataset] = []

for row in rows:
    dataset = Dataset(
        dataset_id=row[0],
        name=row[1],
        size_bytes=row[2],
        rows=row[3],
        source=row[4],
    )
    datasets.append(dataset)

st.subheader(f"Available Datasets ({len(datasets)})")

for ds in datasets:
    size_mb = ds.calculate_size_mb() 
    
    with st.expander(f"**Dataset {ds._id}: {ds._name}**"):
        st.write(f"**Source:** {ds.get_source()}")
        st.write(f"**Size:** {size_mb:.2f} MB")
        st.write(f"**Row Count:** {ds._rows}")
        st.write(str(ds)) 
