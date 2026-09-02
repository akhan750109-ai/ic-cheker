import streamlit as st
import re
import os

# Page Config
st.set_page_config(page_title="IC SPEC FINDER PRO", page_icon="⚡", layout="centered")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #0f172a; font-family: 'Segoe UI', sans-serif; }
    .title-text { font-size: 34px; font-weight: 900; text-align: center; color: #38bdf8; }
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
st.markdown('<div class="sub-text">Mobile IC Hardware Specification Decoder</div>', unsafe_allow_html=True)

# Custom Parser for your ic_database.py file
@st.cache_data
def load_ic_database():
    db = {}
    db_filename = "ic_database.py"
    
    if not os.path.exists(db_filename):
        return db

    with open(db_filename, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            clean_line = line.strip()
            # Skip empty lines or header/comment lines
            if not clean_line or clean_line.startswith("#") or "IC Code" in clean_line:
                continue
            
            # Split line by spaces or tabs
            parts = clean_line.split()
            if len(parts) >= 2:
                # The first word is always the IC Part Code
                ic_code = parts[0].strip().upper().replace('"', '').replace("'", "").replace(",", "")
                rest_of_line = " ".join(parts[1:])
                db[ic_code] = rest_of_line

    return db

IC_DB = load_ic_database()

# Exact Search & Specs Extraction
def find_ic_specs(user_input):
    clean_input = user_input.strip().upper().replace("-", "")
    if not clean_input:
        return None, None, None

    # Search in Parsed File Database
    if clean_input in IC_DB:
        row_text = IC_DB[clean_input]
        
        # 1. Extract Storage (e.g. 32GB, 64GB, 128GB, 256GB)
        storage_match = re.search(r'(\d+\s*GB|\d+\s*TB)', row_text, re.IGNORECASE)
        storage = storage_match.group(1).upper() if storage_match else "Storage Not Mentioned"
        
        # 2. Extract RAM (e.g. 2GB, 3GB, 4GB, 6GB, 8GB)
        # Search specifically near RAM keywords or secondary GB match
        gb_matches = re.findall(r'(\d+\s*GB)', row_text, re.IGNORECASE)
        if len(gb_matches) >= 2:
            ram = gb_matches[1].upper()
        elif "NO RAM" in row_text.upper() or "PURE FLASH" in row_text.upper():
            ram = "No RAM (Pure Flash)"
        else:
            ram_match = re.search(r'(\d+\s*GB)\s*(?:RAM|eMCP|uMCP|LPDDR)?', row_text, re.IGNORECASE)
            ram = ram_match.group(1).upper() if ram_match else "No RAM / Check Details"

        # 3. Extract Manufacturer / Brand
        brand = "GENERIC / OTHER"
        row_upper = row_text.upper()
        if "SK HYNIX" in row_upper or "HYNIX" in row_upper:
            brand = "SK HYNIX"
        elif "SAMSUNG" in row_upper or "SEC" in row_upper:
            brand = "SAMSUNG (SEC)"
        elif "MICRON" in row_upper:
            brand = "MICRON"
        elif "TOSHIBA" in row_upper or "KIOXIA" in row_upper:
            brand = "TOSHIBA / KIOXIA"
        elif "SANDISK" in row_upper:
            brand = "SANDISK"

        return brand, ram, storage

    return "NOT IN DATABASE", "Code Not Listed", "Code Not Listed"

# UI Layout
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="e.g. H9TQ26ADFTBCUR, KMR5B0001M, THGAF4G9N4LBAIR...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = find_ic_specs(user_input)
        st.divider()
        st.subheader(f"🏷️ BRAND: {brand}")
        col1, col2 = st.columns(2)
        with col1: st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2: st.metric(label="💾 INTERNAL STORAGE", value=storage)