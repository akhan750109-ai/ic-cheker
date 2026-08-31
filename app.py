import streamlit as st
import re

# Page Configuration
st.set_page_config(
    page_title="IC SPEC FINDER PRO", 
    page_icon="⚡", 
    layout="centered"
)

# Custom Styling (Dark Mode Modern UI)
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; font-family: 'Segoe UI', sans-serif; }
    .title-text { font-size: 36px; font-weight: 900; text-align: center; color: #38bdf8; }
    .sub-text { font-size: 14px; text-align: center; color: #94a3b8; margin-bottom: 25px; }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0284c7 0%, #6366f1 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 10px !important;
        border-radius: 8px !important;
        border: none !important;
    }
    .stTextInput input {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        background-color: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        text-align: center;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">⚡ IC SPEC FINDER PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Professional Mobile IC Hardware Decoder</div>', unsafe_allow_html=True)

# 1. Database Loading Function (ic_database.py se data read karna)
@st.cache_data
def load_database():
    parsed_db = {}
    
    # Try importing dictionary format
    try:
        import ic_database
        if hasattr(ic_database, 'EXACT_IC_DB') and isinstance(ic_database.EXACT_IC_DB, dict):
            for k, v in ic_database.EXACT_IC_DB.items():
                parsed_db[str(k).strip().upper()] = v
            return parsed_db
    except Exception:
        pass

    # Read raw text or table lines if dictionary format fails
    try:
        with open("ic_database.py", "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                line_clean = line.strip()
                if not line_clean or line_clean.startswith("#") or line_clean.startswith("EXACT_IC_DB"):
                    continue
                
                # Split line into components
                parts = line_clean.split()
                if len(parts) >= 2:
                    code = parts[0].strip().upper().replace('"', '').replace("'", "").replace(",", "")
                    rest_of_line = " ".join(parts[1:])
                    parsed_db[code] = rest_of_line
    except Exception:
        pass

    return parsed_db

IC_DB = load_database()

# 2. Main Search Logic (Matching Logic)
def decode_ic(code):
    clean = code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None

    # --- MATCH LEVEL 1: Exact Code Match in DB ---
    if clean in IC_DB:
        val = IC_DB[clean]
        if isinstance(val, tuple):
            # Tuple Format: (RAM, Storage, Brand)
            return val[2], val[0], val[1]
        elif isinstance(val, str):
            # Parse text string format
            raw_text = val.upper()
            
            # Brand identification
            brand = "SAMSUNG (SEC)" if ("SAMSUNG" in raw_text or "SEC" in raw_text or clean.startswith("K")) else "GENERIC / OTHER"
            if "HYNIX" in raw_text or clean.startswith(("H9", "H5")): brand = "SK HYNIX"
            elif "MICRON" in raw_text or clean.startswith(("JZ", "NW", "MT")): brand = "MICRON"
            elif "SANDISK" in raw_text or clean.startswith("SDIN"): brand = "SANDISK"

            # Storage extraction
            match_storage = re.search(r'(\d+\s*GB|\d+\s*TB)', raw_text)
            storage = match_storage.group(1) if match_storage else "Unknown Storage"

            # RAM extraction
            match_ram = re.search(r'(\d+\s*GB)\s*(?:RAM|LPDDR|eMCP|uMCP)', raw_text)
            if match_ram:
                ram = match_ram.group(1)
            elif "EMMC" in raw_text or "UFS" in raw_text:
                ram = "No RAM (Pure Flash)"
            else:
                ram = "Standard RAM"

            return brand, ram, storage

    # --- MATCH LEVEL 2: Sub-String / Partial Match ---
    for key, val in IC_DB.items():
        if key in clean or clean in key:
            if isinstance(val, tuple):
                return val[2], val[0], val[1]

    # --- MATCH LEVEL 3: Samsung Nomenclature Fallback ---
    if clean.startswith("K"):
        brand = "SAMSUNG (SEC)"
        if "KLUDG" in clean:
            return brand, "No RAM (Pure Flash)", "128 GB UFS 2.1"
        elif "KLUCG" in clean:
            return brand, "No RAM (Pure Flash)", "64 GB UFS 2.0/2.1"
        elif "KLUFG" in clean:
            return brand, "No RAM (Pure Flash)", "512 GB UFS 3.1"
        elif "KLMDG" in clean:
            return brand, "No RAM (Pure Flash)", "128 GB eMMC 5.1"
        elif "KLMCG" in clean:
            return brand, "No RAM (Pure Flash)", "64 GB eMMC 5.1"
        elif "KLMBG" in clean:
            return brand, "No RAM (Pure Flash)", "32 GB eMMC 5.1"
        elif "KM5V7" in clean or "KM5V8" in clean:
            return brand, "6 GB / 8 GB LPDDR4X", "128 GB uMCP"

    # Fallback when code is completely absent from file
    return "GENERIC / UNKNOWN", "Unknown RAM", "Unknown Storage"

# 3. User Interface
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="e.g. KLUDG4U1EA, H9TQ26ADFTAC, KMRP60014M...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = decode_ic(user_input)
        st.divider()
        st.subheader(f"🏷️ BRAND: {brand}")
        col1, col2 = st.columns(2)
        with col1: st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2: st.metric(label="💾 INTERNAL STORAGE", value=storage)