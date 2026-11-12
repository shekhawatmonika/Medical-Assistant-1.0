import streamlit as st
from rag import RAGEngine
from database import create_database, create_appointment, get_appointments
from api_client import search_fda
from llm import generate_answer

st.set_page_config(page_title="Medical Assistant", page_icon="🏥", layout="wide")

@st.cache_resource
def load_rag():
    return RAGEngine()

rag = load_rag()
create_database()

st.title("🏥 Medical Assistant")
st.caption("Streamlit + RAG + SQLite + Public API + Ollama/Llama 3.2")

st.warning("Educational/administrative demo only. This assistant does not diagnose diseases, prescribe medicines, or provide emergency treatment.")

with st.sidebar:
    st.header("⚙️ Components")
    st.write("✅ Streamlit")
    st.write("✅ RAG + ChromaDB")
    st.write("✅ Local Embeddings")
    st.write("✅ SQLite")
    st.write("✅ Ollama + Llama 3.2")
    st.write("✅ Public openFDA API")
    st.divider()

    st.header("📅 Book Appointment")
    patient_name = st.text_input("Patient Name")
    department = st.selectbox("Department", ["Cardiology", "Dermatology", "General Medicine"])
    doctor = st.text_input("Doctor")
    appointment_date = st.date_input("Appointment Date")
    appointment_time = st.time_input("Appointment Time")

    if st.button("Book Appointment", use_container_width=True):
        if not patient_name.strip() or not doctor.strip():
            st.error("Please enter patient name and doctor.")
        else:
            appointment_id = create_appointment(patient_name, department, doctor, str(appointment_date), str(appointment_time))
            st.success(f"Appointment booked. ID: {appointment_id}")

st.header("💬 Ask the Medical Assistant")
question = st.text_area("Your question", placeholder="Example: Which department handles heart related consultations?", height=120)

if st.button("Ask Assistant", type="primary", use_container_width=True):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching documents and generating answer..."):
            try:
                documents, metadata = rag.search(question)
                rag_context = "\n\n".join(documents)
                appointments = get_appointments()
                database_context = "\n".join(str(row) for row in appointments)

                api_context = ""
                if any(word in question.lower() for word in ["drug", "medicine", "medication"]):
                    api_context = str(search_fda(question))

                answer = generate_answer(question, rag_context, database_context, api_context)
                st.subheader("🤖 Answer")
                st.write(answer)

                st.subheader("📚 Retrieved Sources")
                for item in metadata:
                    st.write(f"📄 {item.get('source', 'Unknown')}")
            except Exception as exc:
                st.error("Could not generate an answer. Make sure Ollama is installed and Llama 3.2 is available.")
                st.exception(exc)

st.divider()
st.header("📋 Appointment Records")

if st.button("Refresh Appointments"):
    rows = get_appointments()
    if rows:
        for row in rows:
            appointment_id, patient, department, doctor, date, time, status = row
            with st.expander(f"#{appointment_id} — {patient} — {department}"):
                st.write(f"**Doctor:** {doctor}")
                st.write(f"**Date:** {date}")
                st.write(f"**Time:** {time}")
                st.write(f"**Status:** {status}")
    else:
        st.info("No appointments found.")
