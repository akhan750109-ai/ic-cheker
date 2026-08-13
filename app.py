import streamlit as st
import pandas as pd
import os
import google.generativeai as genai

# Configure Gemini AI with your API Key
GEMINI_API_KEY = "AIzaSyCKTYBOs6Ro0IYwzR1oHQxfHBD45YsAEZY"
genai.configure(api_key=GEMINI_API_KEY)

# Database Configuration
DATABASE_PATH = "database.csv"

@st.cache_data
def load_database():
    if os.path.exists(DATABASE_PATH):
        try:
            # on_bad_lines='skip' खराब लाइनों की वजह से ऐप को क्रैश होने से रोकेगा
            df = pd.read_csv(DATABASE_PATH, on_bad_lines='skip')
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            st.error(f"Error loading database: {e}")
            return pd.DataFrame()
    return pd.DataFrame()

def find_match_in_csv(query: str, database: pd.DataFrame):
    if database.empty or "Code" not in database.columns:
        return None
    
    clean_query = str(query).strip().upper()
    database_codes = database["Code"].astype(str).str.strip().str.upper()
    matched_rows = database[database_codes == clean_query]
    
    if not matched_rows.empty:
        return matched_rows
    return None

def search_with_ai(query: str):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        prompt = f"""
        You are an expert mobile hardware and scrap PCB component identifier.
        Look up the following mobile IC/PCB part number or code: '{query}'
        
        Provide the output strictly in this simple format:
        - *Brand/Manufacturer*: (e.g. Samsung, MediaTek, Qualcomm, SK Hynix, etc.)
        - *CPU / Component Name*: (Full name or description)
        - *RAM / Storage*: (e.g. 4GB/64GB or N/A)
        - *Component Type*: (e.g. eMMC, eMCP, UFS, Power IC, CPU, Audio IC)
        - *Scrap Grade Category*: (Grade A, B, or C based on general scrap market value)

        If you don't find exact details, provide the closest known specifications for this chip/code.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI सर्च करने में समस्या आई: {e}"

def display_csv_match(result: pd.DataFrame, matched_code: str):
    row = result.iloc[0]
    st.success(f"✅ डेटाबेस (CSV) में मैच मिला: *{matched_code}*")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Code", row.get("Code", "N/A"))
        st.metric("CPU / Chip", row.get("CPU", "N/A"))
    with col2:
        st.metric("RAM / ROM", row.get("RAM_ROM", "N/A"))
        st.metric("Grade", row.get("Grade", "N/A"))

def run_lookup(query: str, database: pd.DataFrame):
    if not query.strip():
        st.warning("कृपया कोई IC या PCB कोड टाइप करें।")
        return

    # Step 1: Check Local CSV Database
    csv_match = find_match_in_csv(query, database)
    
    if csv_match is not None:
        display_csv_match(csv_match, query)
    else:
        # Step 2: Fallback to AI Search if not in CSV
        st.info(f"🔍 '{query}' लोकल डेटाबेस में नहीं मिला। AI द्वारा खोजा जा रहा है...")
        with st.spinner("AI डेटा ढूँढ रहा है..."):
            ai_result = search_with_ai(query)
            st.subheader(f"🤖 AI खोज परिणाम: {query}")
            st.markdown(ai_result)

def main():
    st.set_page_config(page_title="Mobile Scrap PCB & IC Identifier", page_icon="🔍", layout="wide")
    st.title("📱 Mobile Scrap PCB & IC Identifier")
    st.caption("आपकी अपनी CSV फ़ाइल + AI सर्च इंटीग्रेशन")

    database = load_database()

    tab_manual, tab_photo = st.tabs(["Manual IC Code Search", "Photo Upload"])

    with tab_manual:
        st.subheader("IC या PCB कोड खोजें")
        query_input = st.text_input("Enter PCB / IC Code:", placeholder="e.g. 32EMCP16, MT6739, SDM450")
        if st.button("Search Code"):
            run_lookup(query_input, database)

    with tab_photo:
        st.subheader("Upload PCB Photo")
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
            st.info("Photo processing feature (EasyOCR) coming soon...")
if __name__=="__main__": main()