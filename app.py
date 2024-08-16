# Import the necessary libraries/modules
import streamlit as st
from txtai.pipeline import Summary
from PyPDF2 import PdfReader
from gtts import gTTS
import os

# Set the page configuration
st.set_page_config(layout="wide")

@st.cache_resource
def summary_text(text):
    # Create a summary object and summarize the text
    summary = Summary()
    result = summary(text)
    return result

def extract_text_from_pdf(file_path):
    # Extract text from the PDF file using PyPDF2
    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        page = reader.pages[0]
        text = page.extract_text()
    return text

def text_to_speech(text, filename, lang='en'):
    # Create text-to-speech model and save the audio file
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

# Sidebar selection box for language/accent
voice_choice = st.sidebar.selectbox("Select voice", ["English (US)", "English (UK)", "English (Australia)", "English (India)", "French", "German", "Spanish"])

# Map the selection to language codes
voice_map = {
    "English (US)": "en",
    "English (UK)": "en-uk",
    "English (Australia)": "en-au",
    "English (India)": "en-in",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}

selected_voice = voice_map[voice_choice]

# Sidebar selection box
choice = st.sidebar.selectbox("Select your choice", ["Summarize Text", "Summarize Document"])

if choice == "Summarize Text":
    st.subheader("Summarize Text using txtai")
    input_text = st.text_area("Enter your text here")
    if input_text:
        if st.button("Summarize Text"):
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown("**Your Input Text**")
                st.markdown(f'<div style="color: lightgray;">{input_text}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Summary Result**")
                result = summary_text(input_text)
                st.markdown(f'<div style="color: lightgreen;">{result}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown("**Text-to-Speech**")
                # Convert summarized text to speech and save as an audio file
                audio_file = "summarized_output.mp3"
                text_to_speech(result, audio_file, lang=selected_voice)
                # Play the audio file in Streamlit
                st.audio(audio_file)
                # Clean up the audio file after use
                if os.path.exists(audio_file):
                    os.remove(audio_file)
    else:
        st.warning("No text entered")

elif choice == "Summarize Document":
    st.subheader("Summarize Document using txtai")
    input_file = st.file_uploader("Upload your document here", type=['pdf'])
    if input_file:
        if st.button("Summarize Document"):
            with open("doc_file.pdf", "wb") as f:
                f.write(input_file.getbuffer())
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.markdown("**Extracted Text from Document**")
                extracted_text = extract_text_from_pdf("doc_file.pdf")
                st.markdown(f'<div style="color: lightgray;">{extracted_text}</div>', unsafe_allow_html=True)
            with col2:
                st.markdown("**Summary Document**")
                summary_result = summary_text(extracted_text)
                st.markdown(f'<div style="color: lightgreen;">{summary_result}</div>', unsafe_allow_html=True)
            with col3:
                st.markdown("**Text-to-Speech**")
                # Convert summarized text to speech and save as an audio file
                audio_file = "summarized_output.mp3"
                text_to_speech(summary_result, audio_file, lang=selected_voice)
                # Play the audio file in Streamlit
                st.audio(audio_file)
                # Clean up the audio file after use
                if os.path.exists(audio_file):
                    os.remove(audio_file)
    else:
        st.warning("No document uploaded")
