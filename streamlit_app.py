import streamlit as st
from openai import OpenAI
from smartgc import smartgc

st.title("SmartGC")
st.write(
    "Upload a FASTA file below or copy-paste the sequences directly. "
)

uploaded_file = st.file_uploader(
    "Upload a FASTA file", type=("fasta")
)

text = st.text_area(
    "Or copy-paste the sequences directly",


)
fasta = None
if uploaded_file is not None:
    fasta = uploaded_file.read()


elif text is not None:
    fasta = text

# Call the `smartgc` function with the `fasta` variable. While it is running, display a message. When it is done, display the result.
with st.spinner("Calculating GC content..."):
    result = smartgc(fasta)
    st.write(result)
