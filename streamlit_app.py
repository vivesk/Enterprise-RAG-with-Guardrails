import requests
import streamlit as st


API_URL = st.sidebar.text_input("API URL", "http://127.0.0.1:8000")

st.title("Enterprise RAG Assistant")
st.caption("Day 1 AI Engineer interview project")

uploaded = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded and st.button("Index document"):
    response = requests.post(
        f"{API_URL}/ingest",
        files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")},
        timeout=120,
    )
    if response.ok:
        st.success(response.json())
    else:
        st.error(response.text)

question = st.text_input("Ask a question about the indexed document")

if st.button("Ask") and question:
    response = requests.post(
        f"{API_URL}/ask",
        json={"question": question},
        timeout=120,
    )

    if response.ok:
        result = response.json()

        if result["blocked"]:
            st.error(result["answer"])
        else:
            st.markdown("### Answer")
            st.write(result["answer"])
            st.markdown("### Retrieved Sources")
            for source in result["sources"]:
                st.write(
                    f"- {source['source']} | {source['chunk_id']} "
                    f"| distance={source['distance']:.4f}"
                )
    else:
        st.error(response.text)
