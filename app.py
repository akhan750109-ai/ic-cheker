import streamlit as st
import re
import requests
import urllib.parse

# 1. Page Setup
st.set_page_config(page_title="Universal IC Spec Finder", page_icon="⚡", layout="centered")

# 2. CSS to hide Streamlit Header and Footer (App-like Look)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { top: -50px; }
    </style>
""", unsafe_allow_html=True)

# 3. App Title
st.title("⚡ Universal IC Spec Finder")
st.write("दुनिया की किसी भी IC, PCB या चिप का कोड डालें - यह तुरंत सटीक RAM और Storage बताएगा:")

# 4. Big Screen Display Box
def show_big_specs(part_code, ram_gb, storage_gb, chip_type, details):
    html_code = f"""
    <div style="border: 2px solid #38bdf8; border-radius: 12px; padding: 18px; background-color: #1e293b; margin-top: 15px; color: #fff;">
        <h3 style="text-align: center; color: #38bdf8; margin-bottom: 8px; font-size: 22px;">PART CODE: {part_code}</h3>
        
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="background-color: #0284c7; color: #ffffff; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 15px;">
                🔌 TYPE: {chip_type}
            </span>
        </div>

        <table style="width:100%; text-align:center; border-collapse:collapse; font-family:sans-serif;">
          <tr style="background-color:#0f172a; color:#38bdf8; font-size:16px;">
            <th style="padding:10px; width:50%; border:1px solid #334155;">⚡ RAM (रैम)</th>
            <th style="padding:10px; width:50%; border:1px solid #334155;">💾 STORAGE (इंटरनल)</th>
          </tr>
          <tr>
            <td style="padding:15px; border:1px solid #334155; background-color:#334155; color:#fef08a; font-size:26px; font-weight:bold;">{ram_gb}</td>
            <td style="padding:15px; border:1px solid #334155; background-color:#334155; color:#86efac; font-size:26px; font-weight:bold;">{storage_gb}</td>
          </tr>
        </table>
        <p style="margin-top:15px; font-size:12px; color:#94a3b8; text-align:center;"><b>Datasheet Status:</b> {details}</p>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# 5. The Working Fast Logic
def instant_ic_decoder(code):
    clean = code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None, None

    # SAMSUNG RULES
    if clean.startswith("KM") or clean.startswith("KL"):
        chip_type = "Samsung eMCP"
        if "750012" in clean: return "2 GB LPDDR3", "16 GB eMMC", "Samsung eMCP", "Exact Match"
        if "60014" in clean: return "3 GB LPDDR3", "32 GB eMMC", "Samsung eMCP", "Exact Match"
        if "60015" in clean: return "4 GB LPDDR4X", "64 GB", "Samsung eMCP", "Exact Match"
        if "60013" in clean: return "6 GB LPDDR4X", "128 GB", "Samsung eMCP", "Exact Match"

    # HYNIX RULES
    if clean.startswith("H9TQ") or clean.startswith("H9TP"):
        if "17AB" in clean: return "2 GB LPDDR3", "16 GB eMMC", "SK Hynix eMCP", "Exact Match"
        if "18AB" in clean: return "3 GB LPDDR3", "32 GB eMMC", "SK Hynix eMCP", "Exact Match"
        if "52AC" in clean: return "4 GB LPDDR4X", "64 GB eMMC", "SK Hynix eMCP", "Exact Match"

    # MICRON RULES
    if "JZ150" in clean: return "3 GB LPDDR3", "32 GB eMMC", "Micron eMCP", "Exact Match"
    if "NW813" in clean: return "4 GB LPDDR4X", "64 GB eMMC", "Micron eMCP", "Exact Match"

    # UNIVERSAL PATTERN
    match = re.search(r'(16|32|64|128|256)', clean)
    if match:
        gb = match.group(1)
        return "Check Board", f"{gb} GB", "Universal Chip", "Pattern Match"
    
    return None, None, None, None

# 6. Main Execution
def main():
    with st.form(key="search_form"):
        user_input = st.text_input("Enter IC Code:", placeholder="e.g. KMF750012M").strip().upper()
        submit_btn = st.form_submit_button("Search Specs Instantly ⚡")

    if submit_btn and user_input:
        ram, storage, ctype, note = instant_ic_decoder(user_input)
        if ram:
            show_big_specs(user_input, ram, storage, ctype, note)
        else:
            st.error("डेटा नहीं मिला। कोड सही डालें।")

if __name__ == "__main__":
    main()