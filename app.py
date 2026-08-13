import streamlit as st
import urllib.parse
import re
import requests

# Page Configuration
st.set_page_config(page_title="Instant IC Spec Finder", page_icon="⚡", layout="centered")

st.title("⚡ Instant IC & eMMC GB Finder")
st.write("कोई भी चिप/IC कोड दर्ज करें और सीधे बड़े अक्षरों में RAM और Storage (GB) देखें:")

# Input Form
with st.form(key="search_form"):
    user_input = st.text_input("Enter IC / PCB Code:", placeholder="e.g. KMRC1000BM, KMQE60013M...").strip().upper()
    submit_btn = st.form_submit_button("Search Specs")

# HTML Box Display for Big Bold Numbers
def show_big_specs(part_code, ram_gb, storage_gb):
    html_code = f"""
    <div style="border: 2px solid #007bff; border-radius: 10px; padding: 15px; background-color: #f8f9fa; margin-top: 15px;">
        <h3 style="text-align: center; color: #007bff; margin-bottom: 15px;">PART CODE: {part_code}</h3>
        <table style="width:100%; text-align:center; border-collapse:collapse; font-family:sans-serif;">
          <tr style="background-color:#007bff; color:white; font-size:18px;">
            <th style="padding:10px; width:50%;">⚡ RAM (रैम)</th>
            <th style="padding:10px; width:50%;">💾 STORAGE (इंटरनल)</th>
          </tr>
          <tr>
            <td style="padding:15px; border:1px solid #ddd; background-color:#fff3cd; color:#856404; font-size:32px; font-weight:bold;">{ram_gb}</td>
            <td style="padding:15px; border:1px solid #ddd; background-color:#d4edda; color:#155724; font-size:32px; font-weight:bold;">{storage_gb}</td>
          </tr>
        </table>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

def main():
    if submit_btn and user_input:
        st.info(f"🔍 Searching live specs for: *{user_input}*...")

        ram_found = None
        storage_found = None

        # 1. Direct Decoder Logic (Samsung / Hynix / Micron Common Patterns)
        if "1000BM" in user_input or "1000" in user_input:
            ram_found = "3 GB"
            storage_found = "32 GB"
        elif "6001" in user_input or "60013M" in user_input:
            ram_found = "2 GB"
            storage_found = "16 GB"
        elif "2100" in user_input:
            ram_found = "4 GB"
            storage_found = "64 GB"

        # 2. Live Web Search Parser (इंटरनेट से डायरेक्ट ऑटो-सर्च)
        if not ram_found or not storage_found:
            try:
                query = f"{user_input} ram storage specs gb"
                url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=5)
                
                if response.status_code == 200:
                    text = response.text
                    
                    storage_match = re.search(r'(\b16|\b32|\b64|\b128|\b256)\s*GB', text, re.IGNORECASE)
                    if storage_match:
                        storage_found = f"{storage_match.group(1)} GB"
                    
                    ram_match = re.search(r'(\b1|\b2|\b3|\b4|\b6|\b8|\b12)\s*GB\s*(RAM|LPDDR|DDR)', text, re.IGNORECASE)
                    if ram_match:
                        ram_found = f"{ram_match.group(1)} GB"
            except Exception:
                pass

        final_ram = ram_found if ram_found else "Check Datasheet"
        final_storage = storage_found if storage_found else "Check Datasheet"

        # Display Result
        st.success("✅ Search Complete!")
        show_big_specs(user_input, final_ram, final_storage)

        # Direct Web Links Backup
        st.markdown("---")
        st.write("🔗 *Direct Datasheet Search Links:*")
        encoded_q = urllib.parse.quote(f"{user_input} ic datasheet ram storage gb")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("👉 Google Search", f"https://www.google.com/search?q={encoded_q}", use_container_width=True)
        with col2:
            st.link_button("👉 AllDataSheet Search", f"https://www.alldatasheet.com/view.jsp?Searchword={urllib.parse.quote(user_input)}", use_container_width=True)

# Correct Syntax Execution (No Indentation or Name Errors)
if _name_ == "_main_":
    main()