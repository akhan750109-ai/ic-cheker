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
# COMBINED COMPLETE DATABASE (PREVIOUS + NEW DATA)
# ----------------------------------------------------
RAW_DATABASE_TEXT = """
KLM4G1FETE 4GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMAG1JENB 16GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMAG1JETD 16GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMAG2GE4A 16GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMAG2GEAC 16GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMAG2GEND 16GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMAG2GESD 16GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMAG2JENB 16GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMAG4FEJA 16GB - eMMC 5.0 Samsung (SEC) 153FBGA
KMF820012M 16GB 2GB eMCP (eMMC+LPDDR2) Samsung (SEC) 169FBGA
KMQ310013A 16GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ310013B 16GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ310013M 16GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ820013M 16GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ8X000SA 16GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQE60013M 16GB 1.5GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR21000BM 16GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR310001M 16GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR31000BA 16GB 3GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR820001M 16GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KLMBG2JENB 32GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMBG4GE4A 32GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMBG4GEND 32GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMBG4JENB 32GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMBG4JETD 32GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMCG4JENB 32GB - eMMC 5.0 Samsung (SEC) 153FBGA
KMQ210013M 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ72000SM 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMQ7X0013M 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMR4B0001M 32GB 3GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMRH60014M 32GB 3GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
KMRX1000BMA 32GB 2GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KLMCG4JETD 64GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMCG8GE4A 64GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMCG8GEND 64GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLMCG8JENB 64GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLUCG2K1EA 64GB - UFS 2.0 Samsung (SEC) 254FBGA
KLUCG4J1ED 64GB - UFS 2.1 Samsung (SEC) 254FBGA
KMGX6001DM 64GB - UFS 2.1 Samsung (SEC) 254FBGA
KMR5B0001M 64GB 4GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMRC10014M 64GB 4GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
KMRH60014A 64GB 4GB eMCP (eMMC+LPDDR4) Samsung (SEC) 169FBGA
KLMDG4JETD 128GB - eMMC 5.1 Samsung (SEC) 153FBGA
KLMDG8JENB 128GB - eMMC 5.0 Samsung (SEC) 153FBGA
KLUDG4U1EA 128GB - UFS 2.1 Samsung (SEC) 254FBGA
KLUDG8V1EE 128GB - UFS 2.1 Samsung (SEC) 254FBGA
KLUFG4RHDA 128GB - UFS 3.1 Samsung (SEC) 254FBGA
KM5V7001DM 128GB 6GB uMCP (UFS+LPDDR4X) Samsung (SEC) 254FBGA
KM5V8001DM 128GB 8GB uMCP (UFS+LPDDR4X) Samsung (SEC) 254FBGA
KLUFG8RFDA 512GB - UFS 3.1 Samsung (SEC) 254FBGA
MTFC4GMDEA 4GB - eMMC 4.41 Micron 153FBGA
JW810 8GB - eMMC 5.0 Micron 153FBGA
JY121 8GB - eMMC 4.5 Micron 153FBGA
JY167 8GB - eMMC 5.0 Micron 153FBGA
JW836 16GB - eMMC 5.0 Micron 153FBGA
JW856 16GB - eMMC 5.1 Micron 153FBGA
JY058 16GB 1GB eMCP (eMMC+LPDDR3) Micron 153FBGA
JY976 16GB - eMMC 5.1 Micron 153FBGA
JY997 16GB - eMMC 5.1 Micron 153FBGA
JZ881 16GB - eMMC 5.1 Micron 153FBGA
MTFC16GAKAECN 16GB - eMMC 5.0 Micron 153FBGA
MTFC16GAPALBH 16GB - eMMC 5.1 Micron 153FBGA
NW351 16GB - eMMC 5.1 Micron 153FBGA
JW896 32GB - eMMC 5.0 Micron 153FBGA
JWA97 32GB - eMMC 5.1 Micron 153FBGA
JWB18 32GB - eMMC 5.1 Micron 153FBGA
JZ156 32GB - eMMC 5.1 Micron 153FBGA
JZ423 32GB - eMMC 5.1 Micron 153FBGA
JZ616 32GB - eMMC 5.1 Micron 153FBGA
JZ959 32GB - eMMC 5.1 Micron 153FBGA
MTFC32GAKAECN 32GB - eMMC 5.0 Micron 153FBGA
MTFC32GAPALBH 32GB - eMMC 5.1 Micron 153FBGA
NW133 32GB - eMMC 5.1 Micron 153FBGA
NW640 32GB 3GB eMCP (eMMC+LPDDR4) Micron 169FBGA
JWA38 64GB - eMMC 5.1 Micron 153FBGA
JWB27 64GB - eMMC 5.1 Micron 153FBGA
JZ115 64GB - eMMC 5.1 Micron 153FBGA
JZ144 64GB - eMMC 5.1 Micron 153FBGA
JZ380 64GB - eMMC 5.1 Micron 153FBGA
JZ512 64GB - eMMC 5.1 Micron 153FBGA
JZ671 64GB - eMMC 5.1 Micron 153FBGA
MTFC64GAKAECN 64GB - eMMC 5.0 Micron 153FBGA
MTFC64GAPALBH 64GB - eMMC 5.1 Micron 153FBGA
NW262 64GB - eMMC 5.1 Micron 153FBGA
NW643 64GB 4GB eMCP (eMMC+LPDDR4) Micron 169FBGA
JZ067 128GB - eMMC 5.1 Micron 153FBGA
JZ159 128GB - eMMC 5.1 Micron 153FBGA
JZ216 128GB - eMMC 5.1 Micron 153FBGA
JZ341 128GB - eMMC 5.1 Micron 153FBGA
JZ736 128GB - eMMC 5.1 Micron 153FBGA
JZ828 128GB - eMMC 5.1 Micron 153FBGA
MTFC128GAKAECN 128GB - eMMC 5.1 Micron 153FBGA
MTFC128GAPALNS 128GB - eMMC 5.1 Micron 153FBGA
NW267 128GB - eMMC 5.1 Micron 153FBGA
NW658 128GB - eMMC 5.1 Micron 153FBGA
H26M31003GMR 4GB - eMMC 4.5 SK Hynix 153FBGA
H26M41103HPR 8GB - eMMC 5.0 SK Hynix 153FBGA
H26M52103FMR 16GB - eMMC 5.0 SK Hynix 153FBGA
H26M52208FPR 16GB - eMMC 5.1 SK Hynix 153FBGA
H9HP19ABUMMDAR 16GB 2GB eMCP (eMMC+LPDDR4X) SK Hynix 169FBGA
H9TP17A8JDAC 16GB 1GB eMCP (eMMC+LPDDR2) SK Hynix 169FBGA
H9TQ17ABJTAC 16GB - eMMC 5.0 SK Hynix 153FBGA
H9TQ17ABJTBC 16GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ17ABJTMC 16GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ17ADFTMC 16GB 2GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H9TQ17ADFTMCUR 16GB 3GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ17ADJTMC 16GB 2GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H26M64103EMR 32GB - eMMC 5.1 SK Hynix 153FBGA
H28U62301AMR 32GB - UFS 2.1 SK Hynix 254FBGA
H9TP32A8JDAC 32GB 2GB eMCP (eMMC+LPDDR2) SK Hynix 169FBGA
H9TQ18ABJTMC 32GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ26AAETMC 32GB 2GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ACLTMCUR 32GB 4GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ADFTAC 32GB - eMMC 5.0 SK Hynix 153FBGA
H9TQ26ADFTBCUR 32GB 3GB eMCP (eMMC+LPDDR3) SK Hynix 169FBGA
H9TQ26ADFTMC 32GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ27ADFTMC 32GB 3GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H26M78103CCR 64GB - eMMC 5.1 SK Hynix 153FBGA
H9HP52ACPMMDAR 64GB 4GB eMCP (eMMC+LPDDR4X) SK Hynix 169FBGA
H9TQ32A6BTMC 64GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ52ACLTMC 64GB 4GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H26M88002AMR 128GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ64A8GTMC 128GB - eMMC 5.1 SK Hynix 153FBGA
H9TQ64ABJTMC 128GB 4GB eMCP (eMMC+LPDDR4) SK Hynix 169FBGA
H28U74301AMR 256GB - UFS 2.1 SK Hynix 254FBGA
H28U88301AMR 512GB - UFS 3.1 SK Hynix 254FBGA
SDINBDA4-8G 8GB - eMMC 5.1 SanDisk / WD 153FBGA
SDINBDG4-8G 8GB - eMMC 5.0 SanDisk / WD 153FBGA
SDIN9DW4-16G 16GB 1GB eMCP (eMMC+LPDDR3) SanDisk / WD 169FBGA
SDINBDA4-16G 16GB - eMMC 5.1 SanDisk / WD 153FBGA
SDINBDG4-16G 16GB - eMMC 5.0 SanDisk / WD 153FBGA
SDIN9DW4-32G 32GB 2GB eMCP (eMMC+LPDDR3) SanDisk / WD 169FBGA
SDINBDA4-32G 32GB - eMMC 5.1 SanDisk / WD 153FBGA
SDINBDG4-32G 32GB - eMMC 5.0 SanDisk / WD 153FBGA
SDINBDA4-64G 64GB - eMMC 5.1 SanDisk / WD 153FBGA
SDINADF4-128G 128GB - UFS 2.1 SanDisk / WD 254FBGA
SDINBDA4-128G 128GB - eMMC 5.1 SanDisk / WD 153FBGA
SDINADF4-256G 256GB - UFS 2.1 SanDisk / WD 254FBGA
SDINFDO4-256G 256GB - UFS 3.0 SanDisk / WD 254FBGA
SDINFDO4-512G 512GB - UFS 3.1 SanDisk / WD 254FBGA
THGBMAG5A1JBAIR 4GB - eMMC 4.5 Toshiba / Kioxia 153FBGA
THGBMAG6A2JBAIR 8GB - eMMC 4.5 Toshiba / Kioxia 153FBGA
THGBMHG7C1LBAIL 16GB - eMMC 5.1 Toshiba / Kioxia 153FBGA
THGBMJG6C1LBAIL 16GB - eMMC 5.0 Toshiba / Kioxia 153FBGA
THGBMBG8D4KBAIR 32GB 2GB eMCP (eMMC+LPDDR3) Toshiba / Kioxia 169FBGA
THGBMHG8C2LBAIL 32GB - eMMC 5.1 Toshiba / Kioxia 153FBGA
THGBMJG7C2LBAIL 32GB - eMMC 5.0 Toshiba / Kioxia 153FBGA
THGBMHG9C4LBAIR 64GB - eMMC 5.1 Toshiba / Kioxia 153FBGA
THGBMJG8C4LBAU7 64GB - eMMC 5.0 Toshiba / Kioxia 153FBGA
THGAF4G9N4LBAIR 128GB - UFS 2.1 Toshiba / Kioxia 254FBGA
THGBMHT0C8LBAIG 128GB - eMMC 5.1 Toshiba / Kioxia 153FBGA
THGAF8G9T43BAIR 256GB - UFS 3.1 Toshiba / Kioxia 254FBGA
KMF720012M 8GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KMFE10012M 8GB 512MB eMCP (eMMC+LPDDR2) Samsung (SEC) 169FBGA
KMFN10012M 8GB 1GB eMCP (eMMC+LPDDR2) Samsung (SEC) 169FBGA
KMFNX0012M 8GB 1GB eMCP (eMMC+LPDDR2) Samsung (SEC) 169FBGA
KMQE10013M 8GB 1GB eMCP (eMMC+LPDDR3) Samsung (SEC) 169FBGA
KLUEG4U1ED 256GB - UFS 3.0 Samsung (SEC) 254FBGA
KLUEG8U1EA 256GB - UFS 2.1 Samsung (SEC) 254FBGA
KLUFG8RHDA 256GB - UFS 3.1 Samsung (SEC) 254FBGA
KM5V0001DM 256GB 8GB uMCP (UFS+LPDDR4X) Samsung (SEC) 254FBGA
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

# Core IC Search Logic
def search_ic(user_code):
    clean = user_code.strip().upper().replace("-", "")
    if not clean:
        return None, None, None

    matched_text = None
    if clean in IC_DB:
        matched_text = IC_DB[clean]
    else:
        for key in IC_DB:
            if key in clean or clean in key:
                matched_text = IC_DB[key]
                break

    if matched_text:
        row_upper = matched_text.upper()

        # Extract Brand
        brand = "GENERIC / OTHER"
        if "SK HYNIX" in row_upper or "HYNIX" in row_upper: brand = "SK HYNIX"
        elif "SAMSUNG" in row_upper or "SEC" in row_upper: brand = "SAMSUNG (SEC)"
        elif "MICRON" in row_upper: brand = "MICRON"
        elif "TOSHIBA" in row_upper or "KIOXIA" in row_upper: brand = "TOSHIBA / KIOXIA"
        elif "SANDISK" in row_upper or "WD" in row_upper: brand = "SANDISK / WD"

        # Extract Storage and RAM
        gb_matches = re.findall(r'(\d+(?:\.\d+)?\s*(?:GB|MB))', matched_text, re.IGNORECASE)
        
        if len(gb_matches) >= 2:
            storage = gb_matches[0].upper()
            ram = gb_matches[1].upper()
        elif len(gb_matches) == 1:
            storage = gb_matches[0].upper()
            ram = "No RAM (Pure Flash)"
        else:
            storage = "Unknown Storage"
            ram = "Unknown RAM"

        return brand, ram, storage

    return "NOT IN DATABASE", "Code Not Listed", "Code Not Listed"

# UI Layout
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="e.g. KLM4G1FETE, KMQE60013M, MTFC16GAKAECN...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = search_ic(user_input)
        st.divider()
        st.subheader(f"🏷️ BRAND: {brand}")
        col1, col2 = st.columns(2)
        with col1: st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2: st.metric(label="💾 INTERNAL STORAGE", value=storage)