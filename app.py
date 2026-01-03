import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="ICP & Persona Messaging Tool", layout="centered")

# --- DISPLAY LOGO (Centered, Width 100) ---
# We use columns to center the image. 
# The middle column (col2) will hold the image.
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    try:
        # 'use_column_width=False' ensures it uses the explicit width=100
        st.image("logo.png", width=150)
    except:
        st.warning("Logo not found. Upload 'logo.png'.")

# --- Title and Description ---
st.title("ICP & Persona Messaging Tool")
st.markdown("Select an **ICP** and a **Persona** below to generate the specific Workflow Pain and Value Message.")

# --- Load Data ---
@st.cache_data
def load_data():
    filename = 'ICPs x Personas x Workflow Pain x Messaging.csv'
    
    try:
        df = pd.read_csv(filename)
        # CLEANING STEP: Remove rows where 'ICP' is empty (NaN)
        df = df.dropna(subset=['ICP'])
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filename}' was not found. Please ensure it is in the same directory.")
        return pd.DataFrame() 

df = load_data()

if not df.empty:
    # --- Input Section ---
    st.divider()
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        # INPUT 1: Select ICP
        icp_options = df['ICP'].unique()
        selected_icp = st.selectbox("1. Select ICP", options=icp_options)

    with col_input2:
        # INPUT 2: Select Persona
        available_personas = df[df['ICP'] == selected_icp]['Persona'].unique()
        selected_persona = st.selectbox("2. Select Persona", options=available_personas)

    # --- Logic to get output ---
    result_row = df[(df['ICP'] == selected_icp) & (df['Persona'] == selected_persona)]

    # --- Output Section ---
    st.divider()
    
    if not result_row.empty:
        # Extract values
        pain_point = result_row.iloc[0]['Workflow Pain']
        value_message = result_row.iloc[0]['Value Message']

        # Display Output 1: Workflow Pain
        st.subheader("Workflow Pain")
        st.info(**pain_point**)

        # Display Output 2: Value Message
        st.subheader("Value Message")
        st.success(**value_message**)
        
    else:
        st.warning("No data found for this specific combination.")

else:
    st.stop()
