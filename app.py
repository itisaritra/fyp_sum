import streamlit as st
import cohere
import time
import PyPDF2
import docx
from io import StringIO, BytesIO

# Initialize Cohere client
API_KEY = "ms0slgGuFh2udoxiN8zIYPK7RsHRbqU03IQGpBpB"
co = cohere.Client(api_key=API_KEY)

# Define Cohere summarization
def generate_summary_cohere(text, length_option):
    length_mapping = {
        "Short": "short",
        "Medium": "medium",
        "Long": "long"
    }
    length = length_mapping[length_option]

    try:
        response = co.summarize(
            text=text,
            length=length,
            format="paragraph",
            model="summarize-xlarge",
            additional_command="",
            temperature=0.3
        )
        time.sleep(1)
        return response.summary
    except Exception as e:
        return f"An error occurred with Cohere: {e}"

# Extract text from uploaded files
def extract_text(file):
    if file.type == "text/plain":
        return StringIO(file.getvalue().decode("utf-8")).read()
    elif file.type == "application/pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        return None

# Compute Compression Ratio
def compute_compression_ratio(original, summary):
    original_words = len(original.split())
    summary_words = len(summary.split())
    if summary_words == 0:
        return 0
    return original_words / summary_words

# Streamlit App
def main():
    st.set_page_config(page_title="Ensemble Summarization App", page_icon="📝", layout="wide")

    st.markdown("""
        <style>
            .main-header {
                font-size: 2.5em;
                font-weight: bold;
                color: #4CAF50;
                text-align: center;
                margin-bottom: 20px;
            }
            .sub-header {
                text-align: center;
                font-size: 1.2em;
                color: #6c757d;
                margin-bottom: 30px;
            }
        </style>
        <div class="main-header">Ensemble Text Summarization</div>
        <div class="sub-header">
            A Streamlit-based application designed to enhance text summarization accuracy using an advanced ensemble learning approach.
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.header("⚙️ Options")
    length_option = st.sidebar.selectbox("Choose Summary Length:", ("Short", "Medium", "Long"))

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📄 Resources")
    st.sidebar.markdown("- [Project Report](https://drive.google.com/file/d/12iWuXNXkGBNk5PrK6mHJO6RL5Ohwa5jS/view)")
    st.sidebar.markdown("- [Project Presentation](https://summari-wa22e81.gamma.site/)")

    st.sidebar.markdown("---")
    st.sidebar.write("""
        Final Year Project Developed by:  
        - [Aritra Ghosh](https://aritraghosh.co/)  
        - [Subhojit Ghosh](https://subhojit.pages.dev/)  
        Under the mentorship of Dr. Anupam Mondal.
    """)

    st.markdown("### 📂 Upload a File or Enter Text for Summarization")
    uploaded_file = st.file_uploader("Upload a .txt, .docx, or .pdf file:", type=["txt", "docx", "pdf"])
    text = None
    if uploaded_file:
        text = extract_text(uploaded_file)
        if text:
            st.success("✅ File uploaded successfully!")
        else:
            st.error("🚫 Unsupported file type or error reading the file.")

    if not text:
        text = st.text_area("Or enter your text here:", placeholder="Type or paste text here...", height=200)

    if st.button("📝 Generate Summary"):
        if text:
            with st.spinner("Processing... Please wait."):
                progress = st.progress(0)
                for percent in range(1, 101):
                    time.sleep(0.01)
                    progress.progress(percent)

                summary = generate_summary_cohere(text, length_option)

                st.markdown("### 📝 Generated Summary")
                st.text_area("Summary:", summary, height=200)

                # Compression Ratio
                ratio = compute_compression_ratio(text, summary)
                st.markdown(f"**📉 Compression Ratio:** {ratio:.2f} (The summary is {ratio:.2f}× shorter than the original text)")

                # Download Buttons
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button("Download as .txt", data=summary, file_name="summary.txt", mime="text/plain")
                with col2:
                    docx_file = BytesIO()
                    doc = docx.Document()
                    doc.add_paragraph(summary)
                    doc.save(docx_file)
                    docx_file.seek(0)
                    st.download_button(
                        label="Download as .docx",
                        data=docx_file.getvalue(),
                        file_name="summary.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
        else:
            st.error("🚫 Please provide some text or upload a file.")

    st.markdown("---")
    st.markdown("""
        <style>
            .footer {
                text-align: center;
                font-size: 0.9em;
                color: #6c757d;
            }
        </style>
        <div class="footer">
            © 2024 Multi-Model Summarization | All rights reserved.
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
