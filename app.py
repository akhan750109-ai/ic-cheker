import streamlit as st
import re
import importlib

st.set_page_config(page_title="IC SPEC FINDER PRO", page_icon="⚡", layout="centered")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; font-family: 'Segoe UI', sans-serif; }
    .title-text { font-size: 36px; font-weight: 900; text-align: center; color: #38bdf8; }
    .sub-text { font-size: 14px; text-align: center; color: #94a3b8; margin-bottom: 25px; }
    .stButton>button {
        width: 100%; background: linear-gradient(90deg, #0284c7 0%, #6366f1 100%) !important;
        color: white !important; font-size: 18px !important; font-weight: 800 !important;
        padding: 10px !important; border-radius: 8px !important; border: none !important;
    }
    .stTextInput input {
        font-size: 20px !important; font-weight: 800 !important; color: #38bdf8 !important;
        background-color: #1e293b !important; border: 2px solid #38bdf8 !important; text-align: center;
    }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-text">⚡ IC SPEC FINDER PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Database-First Exact Match IC Decoder</div>', unsafe_allow_html=True)

# 1. READ ALL LINES FROM YOUR FILE
def load_database_from_file():
    db = {}
    
    # Method A: Import Dictionary
    try:
        import ic_database
        importlib.reload(ic_database)
        if hasattr(ic_database, 'EXACT_IC_DB') and isinstance(ic_database.EXACT_IC_DB, dict):
            for k, v in ic_database.EXACT_IC_DB.items():
                db[str(k).strip().upper()] = v
            if db: return db
    except Exception:
        pass

    # Method B: Read Raw Lines (Line by Line text)
    try:
        with open("ic_database.py", "r", encoding="utf-8") as f:
            for line in f:
                l = line.strip()
                if not l or l.startswith("#") or "EXACT_IC_DB" in l:
                    continue
                parts = l.split()
                if parts:
                    code = parts[0].replace('"', '').replace("'", "").replace(",", "").strip().upper()
                    db[code] = " ".join(parts[1:])
    except Exception:
        pass

    return db

IC_DB = load_database_from_file()

# 2. EXACT SEARCH ENGINE
def search_ic(user_code):
    clean = user_code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None

    # LEVEL 1: Exact Match in your List
    if clean in IC_DB:
        val = IC_DB[clean]
        
        # If stored as tuple (RAM, Storage, Brand)
        if isinstance(val, tuple):
            return val[2], val[0], val[1]
        
        # If stored as Raw Text
        raw = str(val).upper()
        
        # Brand Detection
        brand = "SAMSUNG (SEC)" if ("SAMSUNG" in raw or "SEC" in raw or clean.startswith("K")) else "GENERIC / OTHER"
        if "HYNIX" in raw or clean.startswith(("H9", "H5")): brand = "SK HYNIX"
        elif "MICRON" in raw or clean.startswith(("JZ", "NW", "MT")): brand = "MICRON"
        elif "SANDISK" in raw or clean.startswith("SDIN"): brand = "SANDISK"

        # RAM Extraction
        ram_found = re.search(r'(\d+\s*GB)\s*(?:RAM|eMCP|uMCP|LPDDR)?', raw)
        if "NO RAM" in raw or "EMMC" in raw or "UFS" in raw:
            if "EMCP" not in raw and "UMCP" not in raw and "LPDDR" not in raw:
                ram = "No RAM (Pure Flash)"
            else:
                ram = ram_found.group(1) if ram_found else "Standard RAM"
        else:
            ram = ram_found.group(1) if ram_found else "Standard RAM"

        # Storage Extraction
        st_found = re.search(r'(\d+\s*GB|\d+\s*TB)', raw)
        storage = st_found.group(1) if st_found else "Storage Not Specified"

        return brand, ram, storage

    # LEVEL 2: Partial Suffix/Prefix Match in List
    for key, val in IC_DB.items():
        if key in clean or clean in key:
            if isinstance(val, tuple):
                return val[2], val[0], val[1]

    # LEVEL 3: Fallback (If code is NOT in your file)
    return "NOT IN DATABASE", "Code Not Listed", "Code Not Listed"

# UI Setup
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="Type your exact IC code here...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = search_ic(user_input)
        st.divider()
        st.subheader(f"🏷️ BRAND: {brand}")
        col1, col2 = st.columns(2)
        with col1: st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2: st.metric(label="💾 INTERNAL STORAGE", value=storage)