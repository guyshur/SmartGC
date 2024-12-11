import streamlit as st
import pandas as pd
from io import StringIO
from smartgc import smartgc

st.title("SmartGC")
if "submit" not in st.session_state:
    st.session_state.submit = False


def submit():
    st.session_state.submit = True


uploaded_file = st.file_uploader(
    "Upload a FASTA file", key="fileuploader")

text = st.text_area(
    "Or copy-paste the sequences directly", key="textarea")

submit_button = st.button("Submit", on_click=submit)

if st.session_state.submit:
    fasta = None
    both = False
    if uploaded_file is not None and text.strip():
        st.warning("Please provide either a FASTA file or text, not both.")
        both = True
    elif uploaded_file is not None:
        fasta = uploaded_file.read()
    elif text.strip():  # Ensure non-empty text
        fasta = text

    if fasta:
        with st.spinner("Calculating GC content..."):
            try:
                # Call the smartgc function
                result = smartgc(fasta)

                # Convert the dictionary to a DataFrame
                df = pd.DataFrame(list(result.items()),
                                  columns=["Sequence_ID", "SmartGC"])

                # Convert the DataFrame to a CSV string
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=True)
                csv_data = csv_buffer.getvalue()

                # Display the result and download button
                st.write("GC Content Results:")
                st.dataframe(df)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="smart_gc_content_results.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error calculating GC content: {e}")
    else:
        if not both:
            st.warning("Please provide a valid FASTA file or text.")

    # Reset after processing
    st.session_state.submit = False
