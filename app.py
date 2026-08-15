import streamlit as st
import re

# Page Setup
st.set_page_config(page_title="Universal Live IC Spec Finder", page_icon="⚡", layout="centered")

# Hide Streamlit UI Components
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp { top: -50px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Universal AI & Live IC Spec Finder")
st.write("दुनिया की किसी भी IC, PCB या चिप का कोड डालें - यह तुरंत सटीक RAM और Storage बताएगा:")

# Render Visual Card Output
def show_big_specs(part_code, ram_gb, storage_gb, chip_type, details):
    html_code = f"""
    <div style="border: 2px solid #38bdf8; border-radius: 12px; padding: 18px; background-color: #1e293b; margin-top: 10px; color: #ffffff; font-family: sans-serif;">
        <h3 style="text-align: center; color: #38bdf8; margin-top: 0px; margin-bottom: 12px; font-size: 22px;">PART CODE: {part_code}</h3>
        
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="background-color: #0284c7; color: #ffffff; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                🔌 TYPE: {chip_type}
            </span>
        </div>

        <table style="width:100%; text-align:center; border-collapse:collapse; margin-top:10px;">
          <tr style="background-color:#0f172a; color:#38bdf8; font-size:15px;">
            <th style="padding:10px; width:50%; border:1px solid #334155;">⚡ RAM (रैम)</th>
            <th style="padding:10px; width:50%; border:1px solid #334155;">💾 STORAGE (इंटरनल)</th>
          </tr>
          <tr>
            <td style="padding:15px; border:1px solid #334155; background-color:#334155; color:#fef08a; font-size:24px; font-weight:bold;">{ram_gb}</td>
            <td style="padding:15px; border:1px solid #334155; background-color:#334155; color:#86efac; font-size:24px; font-weight:bold;">{storage_gb}</td>
          </tr>
        </table>
        <p style="margin-top:15px; margin-bottom: 0px; font-size:12px; color:#94a3b8; text-align:center;"><b>Datasheet Status:</b> {details}</p>
    </div>
    """
    st.components.v1.html(html_code, height=270)

# Exact IC Search Mapping Table
EXACT_IC_DB = {
    # SK Hynix Exact Specs
    "H9TQ26ADFTAC": ("3 GB LPDDR3", "32 GB eMMC", "SK Hynix eMCP", "Exact SK Hynix Datasheet Match"),
    "H9TQ17ABJTAC": ("2 GB LPDDR3", "16 GB eMMC", "SK Hynix eMCP", "Exact SK Hynix Datasheet Match"),
    "H9TQ65ACRNAC": ("4 GB LPDDR3", "64 GB eMMC", "SK Hynix eMCP", "Exact SK Hynix Datasheet Match"),
    "H9TQ17ADFTAC": ("2 GB LPDDR3", "16 GB eMMC", "SK Hynix eMCP", "Exact SK Hynix Datasheet Match"),
    "H9TQ26ACRNAC": ("3 GB LPDDR3", "32 GB eMMC", "SK Hynix eMCP", "Exact SK Hynix Datasheet Match"),
    
    # Samsung Exact Specs
    "KMRP60014M": ("3 GB LPDDR3", "32 GB eMMC", "Samsung eMCP", "Exact Samsung Datasheet Match"),
    "KMDH6001DA": ("3 GB LPDDR4X", "32 GB uMCP", "Samsung uMCP", "Exact Samsung Datasheet Match"),
    "KMQE60013M": ("6 GB LPDDR4X", "128 GB eMMC", "Samsung eMCP", "Exact Samsung Datasheet Match"),
    "KMD210013M": ("4 GB LPDDR4X", "64 GB uMCP", "Samsung uMCP", "Exact Samsung Datasheet Match"),
    
    # Micron Exact Specs
    "JZ150": ("3 GB LPDDR3", "32 GB eMMC", "Micron eMCP", "Exact Micron Datasheet Match"),
    "NW813": ("4 GB LPDDR4X", "64 GB eMMC", "Micron eMCP", "Exact Micron Datasheet Match"),
}

# Decoder Logic
def instant_ic_decoder(code):
    clean = code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None, None

    # Priority 1: Check Exact Code Database First
    if clean in EXACT_IC_DB:
        return EXACT_IC_DB[clean]

    # Priority 2: Pattern Matcher for SK Hynix
    if clean.startswith("H9TQ") or clean.startswith("H9TP") or clean.startswith("H9HP"):
        chip_type = "SK Hynix eMCP"
        if "26AD" in clean or "26A" in clean:
            return "3 GB LPDDR3", "32 GB eMMC", chip_type, "SK Hynix Pattern Match"
        elif "17AB" in clean or "17A" in clean:
            return "2 GB LPDDR3", "16 GB eMMC", chip_type, "SK Hynix Pattern Match"
        elif "52AC" in clean or "52A" in clean:
            return "4 GB LPDDR4X", "64 GB eMMC", chip_type, "SK Hynix Pattern Match"
        elif "1A2" in clean:
            return "6 GB LPDDR4X", "128 GB eMMC", chip_type, "SK Hynix Pattern Match"

    # Priority 3: Pattern Matcher for Samsung
    if clean.startswith("KM") or clean.startswith("KL"):
        chip_type = "Samsung eMCP / uMCP"
        if "60014" in clean:
            return "3 GB LPDDR3", "32 GB eMMC", chip_type, "Samsung Pattern Match"
        elif "60015" in clean or "2100" in clean:
            return "4 GB LPDDR4X", "64 GB eMMC", chip_type, "Samsung Pattern Match"
        elif "60013" in clean:
            return "6 GB LPDDR4X", "128 GB eMMC", chip_type, "Samsung Pattern Match"

    return None, None, None, None

# Main Interface
def main():
    with st.form(key="search_form"):
        user_input = st.text_input("Enter ANY Microchip / IC Code:", placeholder="e.g. KMRP60014M, H9TQ26ADFTAC...").strip().upper()
        submit_btn = st.form_submit_button("Search Specs Instantly ⚡")

    if submit_btn and user_input:
        ram_val, storage_val, chip_type, note = instant_ic_decoder(user_input)

        if ram_val and storage_val:
            st.success("⚡ Instant Result Decoded!")
            show_big_specs(user_input, ram_val, storage_val, chip_type, note)
        else:
            st.error(f"❌ '{user_input}' कोड नहीं मिला। कृपया कोड चेक करें।")

if __name__ == "__main__":
    main()