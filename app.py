import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS

# Page Config
st.set_page_config(page_title="PCB & IC Code Checker", page_icon="⚡", layout="centered")

# 1. Local Database Fast Load
@st.cache_data
def load_data():
    try:
        return pd.read_csv("database.csv")
    except Exception:
        return None

# 2. Instant Local Search Function
def search_local(query, df):
    if not query or not query.strip():
        return None
    query_str = query.strip().lower()
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(query_str, regex=False).any(), axis=1)
    return df[mask]

# 3. Superfast Instant Web Search (No AI Delay, No API Key Error)
def search_web_instant(query):
    try:
        results = []
        search_term = f"{query} IC PCB details datasheet function"
        with DDGS() as ddgs:
            for r in ddgs.text(search_term, max_results=3):
                results.append(r)
        return results
    except Exception as e:
        return None

# Main Application
def main():
    st.title("⚡ Instant PCB & IC Code Checker")

    database = load_data()

    tab_manual, tab_photo = st.tabs(["Manual IC Code", "Upload Photo"])

    with tab_manual:
        st.subheader("IC या PCB कोड खोजें")
        
        # Fast Form Submit
        with st.form(key="search_form"):
            query_input = st.text_input("Enter PCB / IC Code:", placeholder="e.g. NE555, LM358...")
            submit_button = st.form_submit_button(label="Search Code")

        if submit_button and query_input.strip():
            clean_query = query_input.strip()
            
            # Step A: Local Search First
            found_in_local = False
            if database is not None:
                local_results = search_local(clean_query, database)
                if local_results is not None and not local_results.empty:
                    found_in_local = True
                    st.success(f"✅ लोकल डेटाबेस में '{clean_query}' मिला:")
                    st.dataframe(local_results, use_container_width=True)

            # Step B: Fast Web Search if not found in Database
            if not found_in_local:
                st.info(f"🔍 '{clean_query}' लोकल डेटाबेस में नहीं मिला। तुरंत वेब से खोजा जा रहा है...")
                
                web_results = search_web_instant(clean_query)
                
                if web_results:
                    st.success(f"🌐 '{clean_query}' के लिए वेब खोज परिणाम:")
                    for item in web_results:
                        st.markdown(f"*[{item['title']}]({item['href']})*")
                        st.write(item['body'])
                        st.divider()
                else:
                    st.warning("वेब पर तुरंत परिणाम नहीं मिल सका। आप सीधे गूगल पर देख सकते हैं:")
                    st.markdown(f"[👉 Click here to search '{clean_query}' on Google](https://www.google.com/search?q={clean_query}+IC+datasheet)")

    with tab_photo:
        st.subheader("Upload PCB Photo")
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            st.info("Photo processing feature coming soon...")

if _name_ == "_main_":
    main()