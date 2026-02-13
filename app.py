import streamlit as st
import pandas as pd
import re

st.title("Data Recovery Planet - Local Extraction Tool")

uploaded_file = st.file_uploader("Upload Recovered FULL_RECOVERY_DATABASE.csv", type=['csv', 'txt'])

if uploaded_file:
    # 1. Read the file
    content = uploaded_file.getvalue().decode("utf-8", errors="ignore")
    
    # 2. Define our forensic patterns for SME and RN-CBL codes
    rn_pattern = re.compile(r'(RN-CBL-[\d]+).*?Batch-1.*?APS-[\d]+.*?([A-Z\s\.]{5,})', re.I)
    sme_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}).*?(SME-[\d-]+).*?([A-Z\s]{5,})', re.I)
    
    results = []
    
    # 3. Process the 64,118+ lines
    for line in content.splitlines():
        # Find Projects (RN codes)
        for match in rn_pattern.findall(line):
            results.append({'Type': 'PROJECT', 'Date': 'N/A', 'Code': match[0], 'Name': match[1].strip()})
        
        # Find Transactions (SME codes)
        for match in sme_pattern.findall(line):
            results.append({'Type': 'TRANSACTION', 'Date': match[0], 'Code': match[1], 'Name': match[2].strip()})

    if results:
        df = pd.DataFrame(results)
        st.success(f"Successfully extracted {len(df)} valid records!")
        
        # 4. Display a preview of the February 2026 data
        st.subheader("Data Preview")
        st.dataframe(df.head(20)) 
        
        # 5. Download Button for MySQL Import
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned CSV for MySQL",
            data=csv_data,
            file_name="cleaned_recovery_data.csv",
            mime="text/csv"
        )
    else:
        st.error("No valid records found in this file.")
