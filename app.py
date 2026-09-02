import streamlit as st
import re

# Page Configuration
st.set_page_config(page_title="IC SPEC FINDER PRO", page_icon="⚡", layout="centered")

# Visual Styling
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

# ----------------------------------------------------
# DIRECT EMBEDDED DATABASE (No External File Needed)
# ----------------------------------------------------
RAW_DATABASE_TEXT = """
THGAF4G9N4LBAIR 128GB - UFS 2.1 Toshiba / Kioxia 254FBGA
THGBMHT0CBLBAIG 128GB - eMMC 5.1 Toshiba / Kioxia 153FBGA
THGAF8G9T43BAIR 256GB - UFS 3.1 Toshiba / Kioxia 254FBGA
H9TQ64ABJTMC 128GB 4GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H9HP52ACPMMDAR 64GB 4GB eMCP (eMMC+LPDDR4X) SK Hynix 169FBGA
H9TQ52ACLTMC 64GB 4GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
KMR5B0001M 64GB 4GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMRC10014M 64GB 4GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
KMRH60014A 64GB 4GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
NW643 64GB 4GB eMCP (eMMC+LPDDR4) Micron 169FBGA
H9TP32A8JDAC 32GB 2GB eMCP (eMMC+LPDDR2) SK Hynix 169FBGA
H9TQ26AAETMC 32GB 2GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ACLMTA 32GB 4GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ADFTBCUR 32GB 3GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ADFTAC 32GB 3GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ27ADFTMC 32GB 3GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
KMQ210013M 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ72000SM 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ7X0013M 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR4B0001M 32GB 3GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMRH60014M 32GB 3GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
KMRX1000BM 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
NW640 32GB 3GB eMCP (eMMC+LPDDR4) Micron 169FBGA
SDIN9DW4-32G 32GB 2GB eMCP (eMMC+LPDDR3) SanDisk / WD 169FBGA
THGBMBG8D4KBAIR 32GB 2GB uMCP (eMMC+LPDDR3) Toshiba / Kioxia 169FBGA
H9HP19ABUMMDAR 16GB 2GB eMCP (eMMC+LPDDR4X) SK Hynix 169FBGA
H9TP17A8JDAC 16GB 2GB eMCP (eMMC+LPDDR2) SK Hynix 169FBGA
H9TQ17ABJTMC 16GB 2GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H9TQ17ADFTMCUR 16GB 3GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
KLMEG8UCTA 64GB - Pure eMMC 5.1 Samsung (SEC) 153FBGA
KLMEG8U1EM 64GB - Pure eMMC 5.1 Samsung (SEC) 153FBGA
KLMCG2KCTA 64GB - Pure eMMC 5.1 Samsung (SEC) 153FBGA
KLMBG2JETD 32GB - Pure eMMC 5.1 Samsung (SEC) 153FBGA
KLMDG4U1EM 128GB - Pure eMMC 5.1 Samsung (SEC) 153FBGA
KLUDG4U1EA 128GB - Pure UFS 2.1 Samsung (SEC) 153FBGA
KLUCG2KCTA 64GB - Pure UFS 2.1 Samsung (SEC) 153FBGA
KLUFG8RHCF 512GB - Pure UFS 3.1 Samsung (SEC) 153FBGA
"""

@st.cache_data
def build_database():
    db = {}
    lines = RAW_DATABASE_TEXT.strip().split("\n")
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        parts = clean.split()
        if len(parts) >= 2:
            code = parts[0].upper().replace('"', '').replace("'", "").strip()
            rest = " ".join(parts[1:])
            db[code] = rest
    return db

IC_DB = build_database()

# Core IC Search Function
def search_ic(user_code):
    clean = user_code.strip().upper().replace("-", "")
    if not clean:
        return None, None, None

    # Step 1: Direct Database Search
    matched_text = None
    if clean in IC_DB:
        matched_text = IC_DB[clean]
    else:
        # Partial Match (Prefix search)
        for key in IC_DB:
            if key in clean or clean in key:
                matched_text = IC_DB[key]
                break

    if matched_text:
        row_upper = matched_text.upper()

        # 1. Extract Brand
        brand = "GENERIC / OTHER"
        if "SK HYNIX" in row_upper or "HYNIX" in row_upper: brand = "SK HYNIX"
        elif "SAMSUNG" in row_upper or "SEC" in row_upper: brand = "SAMSUNG (SEC)"
        elif "MICRON" in row_upper: brand = "MICRON"
        elif "TOSHIBA" in row_upper or "KIOXIA" in row_upper: brand = "TOSHIBA / KIOXIA"
        elif "SANDISK" in row_upper or "WD" in row_upper: brand = "SANDISK"

        # 2. Extract Storage & RAM
        gb_matches = re.findall(r'(\d+\s*GB|\d+\s*TB)', matched_text, re.IGNORECASE)
        
        if len(gb_matches) >= 2:
            storage = gb_matches[0].upper()
            ram = gb_matches[1].upper()
        elif len(gb_matches) == 1:
            storage = gb_matches[0].upper()
            if "PURE" in row_upper or "EMMC" in row_upper or "UFS" in row_upper:
                ram = "No RAM (Pure Flash Storage)"
            else:
                ram = "RAM Not Specified"
        else:
            storage = "Unknown Storage"
            ram = "Unknown RAM"

        return brand, ram, storage

    # Step 2: Algorithmic Fallback for Samsung Pure Flash (e.g. KLMEG8UCTA)
    if clean.startswith("KL"):
        brand = "SAMSUNG (SEC)"
        ram = "No RAM (Pure Flash Storage)"
        if "8" in clean or "64" in clean: storage = "64 GB"
        elif "4" in clean or "128" in clean: storage = "128 GB"
        elif "2" in clean or "32" in clean: storage = "32 GB"
        else: storage = "eMMC / UFS Storage"
        return brand, ram, storage

    return "NOT IN DATABASE", "Code Not Listed", "Code Not Listed"

# UI Layout
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="e.g. KLMEG8UCTA, H9TQ26ADFTAC...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = search_ic(user_input)
        st.divider()
        st.subheader(f"🏷️ BRAND: {brand}")
        col1, col2 = st.columns(2)
        with col1: st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2: st.metric(label="💾 INTERNAL STORAGE", value=storage)