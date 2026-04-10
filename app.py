import os
import tempfile

import streamlit as st

from pipeline.workflow import rag_pipeline


def save_uploaded_file(uploaded_file):
    suffix = os.path.splitext(uploaded_file.name)[1] or ".mp3"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name


def main():
    st.set_page_config(page_title="Audio Q&A", layout="centered")
    st.title("Audio Question Answering")
    st.write("Upload an audio file, ask a question, and get the answer.")

    uploaded_file = st.file_uploader(
        "Upload audio",
        type=["mp3", "wav", "m4a", "mp4", "mpeg", "mpga"],
    )
    query = st.text_area(
        "Your question",
        placeholder="Example: What is the name of the 2nd speaker?",
        height=120,
    )

    if st.button("Get Answer", type="primary"):
        if uploaded_file is None:
            st.error("Please upload an audio file.")
            return

        if not query.strip():
            st.error("Please enter a question.")
            return

        temp_file_path = save_uploaded_file(uploaded_file)

        try:
            with st.spinner("Transcribing audio and generating answer..."):
                answer = rag_pipeline(query.strip(), temp_file_path)

            st.success("Answer generated successfully.")
            st.subheader("Answer")
            st.write(answer)
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)


if __name__ == "__main__":
    main()
