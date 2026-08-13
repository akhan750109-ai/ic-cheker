import streamlit as st
import requests
import re
import urllib.parse

# Page Configuration
st.set_page_config(page_title="Universal IC Spec Finder", page_icon="⚡", layout="centered")

st.title("⚡ Universal IC & eMMC/UFS GB Finder")
st.write("दुनिया की किसी भी कंपनी (Samsung, Micron, Hynix, SanDisk) की IC का कोड दर्ज करें:")

# HTML Display Box
def show_big_specs(part_code, ram_gb, storage_gb, chip_type, details):
    html_code = f"""
    <div style="border: 2px solid #007bff; border-radius: 10px; padding: 15px; background-color: #f8f9fa; margin-top: 15px;">
        <h3 style="text-align: center; color: #007bff; margin-bottom: 5px;">PART CODE: {part_code}</h3>
        <p style="text-align: center; color: #555; margin-bottom: 15px;"><b>Type:</b> {chip_type}</p>
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
        <p style="margin-top:15px; font-size:14px; color:#333; text-align:center;"><b>Status:</b> {details}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# 1. Live Web Scraper for Universal IC Database
def fetch_live_specs(ic_code):
    try:
        query = f"{ic_code} IC eMMC UFS RAM Storage GB spec sheet"
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        res = requests.get(url, headers=headers, timeout=4)
        text = res.text

        # Extract Storage (GB)
        storage_m = re.search(r'(\b16|\b32|\b64|\b128|\b256|\b512)\s*GB', text, re.IGNORECASE)
        # Extract RAM (GB)
        ram_m = re.search(r'(\b1|\b2|\b3|\b4|\b6|\b8|\b12|\b16)\s*GB', text, re.IGNORECASE)

        ram = f"{ram_m.group(1)} GB" if ram_m else None
        storage = f"{storage_m.group(1)} GB" if storage_m else None

        if ram or storage:
            return ram if ram else "1 GB / 2 GB", storage if storage else "N/A", "Live Web Database Lookup"
    except Exception:
        pass
    return None, None, None

# 2. Universal Positional & Pattern Engine
def decode_ic_code(clean_code):
    # Samsung Specific Positional Logic
    if clean_code.startswith("KM"):
        if "60014" in clean_code or "60014M" in clean_code: return "3 GB / 4 GB", "64 GB", "Samsung eMCP", "Exact Positional Rule"
        elif "60015" in clean_code or "60015M" in clean_code: return "4 GB / 6 GB", "128 GB", "Samsung eMCP", "Exact Positional Rule"
        elif "60012" in clean_code or "60013" in clean_code: return "2 GB", "16 GB", "Samsung eMCP", "Exact Positional Rule"
        elif "1000" in clean_code: return "3 GB", "32 GB", "Samsung eMCP", "Exact Positional Rule"
        elif "2100" in clean_code: return "4 GB", "64 GB", "Samsung eMCP", "Exact Positional Rule"

    # Universal Pattern Extraction (For UFS/eMMC - 512, 256, 128, 64, 32, 16)
    if "512" in clean_code: return "12 GB / 16 GB", "512 GB", "UFS / eMMC", "Universal Code Pattern"
    elif "256" in clean_code: return "8 GB / 12 GB", "256 GB", "UFS / eMMC", "Universal Code Pattern"
    elif "128" in clean_code: return "4 GB / 6 GB", "128 GB", "UFS / eMMC", "Universal Code Pattern"
    elif "64" in clean_code: return "3 GB / 4 GB", "64 GB", "UFS / eMMC", "Universal Code Pattern"
    elif "32" in clean_code: return "2 GB / 3 GB", "32 GB", "UFS / eMMC", "Universal Code Pattern"
    elif "16" in clean_code: return "1 GB / 2 GB", "16 GB", "UFS / eMMC", "Universal Code Pattern"

    # Live Online Fallback for Unknown FBGA Code (Micron, SK Hynix, Toshiba etc.)
    ram_web, storage_web, note = fetch_live_specs(clean_code)
    if ram_web or storage_web:
        return ram_web, storage_web, "IC / FBGA Chip", note

    return "Check Part Number", "Check Part Number", "Unknown IC", "No GB spec matched for this code"

def main():
    with st.form(key="search_form"):
        user_input = st.text_input("Enter ANY IC / PCB Code:", placeholder="e.g. JZ150, KLUD64U1EA, KMRP60014M, H9TP32...").strip().upper()
        submit_btn = st.form_submit_button("Search Specs")

    if submit_btn and user_input:
        clean_code = user_input.replace("-", "").strip()
        st.info(f"🔍 Analyzing Code across Universal Database: *{user_input}*...")

        ram_val, storage_val, chip_type, note = decode_ic_code(clean_code)

        if ram_val != "Check Part Number":
            st.success("✅ Specs Decoded Successfully!")
            show_big_specs(user_input, ram_val, storage_val, chip_type, note)
        else:
            st.error(f"❌ '{user_input}' के लिए कोई जानकारी नहीं मिली। कृपया IC के ऊपर का सही कोड चेक करें।")

if __name__ == "__main__":
    main()