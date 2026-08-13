import streamlit as st
import pandas as pd
import urllib.parse

# 1. Page Configuration
st.set_page_config(page_title="PCB & IC Code Checker", page_icon="⚡", layout="centered")

# 2. Database Load (Caching for speed)
@st.cache_data
def load_data():
    try:
        return pd.read_csv("database.csv")
    except Exception:
        return None

# 3. Fast Local Database Search
def search_local(query, df):
    if not query or not query.strip():
        return None
    query_str = query.strip().lower()
    mask = df.apply(lambda row: row.astype(str).str.lower().str.contains(query_str, regex=False).any(), axis=1)
    return df[mask]

# 4. Main Application Interface
def main():
    st.title("⚡ Fast PCB & IC Code Checker")

    database = load_data()

    tab_manual, tab_photo = st.tabs(["Manual IC Code", "Upload Photo"])

    with tab_manual:
        st.subheader("IC या PCB कोड खोजें")
        
        # Immediate Search Form
        with st.form(key="search_form"):
            query_input = st.text_input("Enter PCB / IC Code:", placeholder="e.g. NE555, LM358...")
            submit_button = st.form_submit_button(label="Search Code")

        if submit_button and query_input.strip():
            clean_query = query_input.strip()
            
            # Step A: Check Local Database First
            found_in_local = False
            if database is not None:
                local_results = search_local(clean_query, database)
                if local_results is not None and not local_results.empty:
                    found_in_local = True
                    st.success(f"✅ डेटाबेस में '{clean_query}' मिला:")
                    st.dataframe(local_results, use_container_width=True)

            # Step B: Instant Direct Web Links (0 Delay, No Module Error)
            if not found_in_local:
                st.warning(f"🔍 '{clean_query}' लोकल डेटाबेस में नहीं मिला।")
                
                encoded_q = urllib.parse.quote(f"{clean_query} IC datasheet pinout details")
                google_url = f"https://www.google.com/search?q={encoded_q}"
                alldatasheet_url = f"https://www.alldatasheet.com/view.jsp?Searchword={urllib.parse.quote(clean_query)}"

                st.markdown("### 🌐 डायरेक्ट वेब परिणाम (Instant Search):")
                col1, col2 = st.columns(2)
                with col1:
                    st.link_button("👉 Google पर खोजें (Datasheet/Pinout)", google_url, use_container_width=True)
                with col2:
                    st.link_button("👉 AllDataSheet पर खोजें", alldatasheet_url, use_container_width=True)

    with tab_photo:
        st.subheader("Upload PCB Photo")
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
            st.info("Photo processing feature coming soon...")
if __name__ == "__main__":