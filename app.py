import streamlit as st
import re

# 1. Page Configuration
st.set_page_config(
    page_title="IC SPEC FINDER PRO", 
    page_icon="⚡", 
    layout="centered"
)

# 2. Modern CSS Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main Title */
    .title-text {
        font-size: 38px;
        font-weight: 900;
        text-align: center;
        color: #38bdf8;
        letter-spacing: 2px;
        margin-bottom: 0px;
    }
    .sub-text {
        font-size: 14px;
        text-align: center;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    /* Big Action Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #0284c7 0%, #6366f1 100%) !important;
        color: white !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        padding: 12px 20px !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(2, 132, 199, 0.4);
        letter-spacing: 1px;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #0369a1 0%, #4f46e5 100%) !important;
        box-shadow: 0 6px 20px rgba(2, 132, 199, 0.6);
    }

    /* Input Field */
    .stTextInput input {
        font-size: 20px !important;
        font-weight: 800 !important;
        color: #38bdf8 !important;
        background-color: #1e293b !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 10px !important;
        text-transform: uppercase;
        text-align: center;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<div class="title-text">⚡ IC SPEC FINDER PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">Professional Mobile IC Hardware Decoder</div>', unsafe_allow_html=True)

# 4. Master Database
EXACT_IC_DB = {
    "H9TQ15ADFTMC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ16ADFTMC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ17ABJTAC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ26ADFTAC": ("3 GB LPDDR3", "32 GB eMMC", "SK HYNIX"),
    "H9TQ65ACRNAC": ("4 GB LPDDR3", "64 GB eMMC", "SK HYNIX"),
    "H54T1A20AFR": ("6 GB LPDDR4X", "128 GB uMCP", "SK HYNIX"),
    "H58T52ACACR": ("4 GB LPDDR4X", "64 GB uMCP", "SK HYNIX"),
    "H58T27ACACR": ("8 GB LPDDR4X", "256 GB uMCP", "SK HYNIX"),
    "KMRP60014M": ("3 GB LPDDR3", "32 GB eMMC", "SAMSUNG"),
    "KMRP60014BM": ("4 GB LPDDR4X", "64 GB eMMC", "SAMSUNG"),
    "KM60014": ("3 GB LPDDR3", "32 GB eMMC", "SAMSUNG"),
    "KMDH6001DA": ("3 GB LPDDR4X", "32 GB uMCP", "SAMSUNG"),
    "KMQE60013M": ("6 GB LPDDR4X", "128 GB eMMC", "SAMSUNG"),
    "KMD210013M": ("4 GB LPDDR4X", "64 GB uMCP", "SAMSUNG"),
    "KMF750012M": ("2 GB LPDDR3", "16 GB eMMC", "SAMSUNG"),
    "KMGD6001BM": ("4 GB LPDDR4X", "64 GB uMCP", "SAMSUNG"),
    "KMDX60018M": ("8 GB LPDDR5", "128 GB uMCP", "SAMSUNG"),
    "KM2V7001CM": ("8 GB LPDDR5", "256 GB uMCP", "SAMSUNG"),
    "JZ150": ("3 GB LPDDR3", "32 GB eMMC", "MICRON"),
    "NW813": ("4 GB LPDDR4X", "64 GB eMMC", "MICRON"),
    "NW814": ("6 GB LPDDR4X", "128 GB uMCP", "MICRON"),
    "SDINADF4128G": ("No RAM", "128 GB eMMC", "SANDISK"),
    "SDINBDG464G": ("No RAM", "64 GB eMMC", "SANDISK")
}

# 5. Decoder Logic
def master_decode_ic(code):
    clean = code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None

    if clean in EXACT_IC_DB:
        ram, storage, brand = EXACT_IC_DB[clean]
        return brand, ram, storage

    for key in EXACT_IC_DB:
        if key in clean or clean in key:
            ram, storage, brand = EXACT_IC_DB[key]
            return brand, ram, storage

    brand = "GENERIC / UNKNOWN"
    ram = "Unknown"
    storage = "Unknown"

    if clean.startswith(("H9", "H5")):
        brand = "SK HYNIX"
        if any(x in clean for x in ["15A", "16A", "17A", "15", "16", "17"]):
            ram, storage = "2 GB LPDDR3", "16 GB eMMC"
        elif any(x in clean for x in ["26A", "27A", "28A", "26", "27"]):
            ram, storage = "3 GB LPDDR3", "32 GB eMMC"
        elif any(x in clean for x in ["52A", "65A", "65", "52"]):
            ram, storage = "4 GB LPDDR4X", "64 GB eMMC"
        elif any(x in clean for x in ["1A2", "1M", "1A"]):
            ram, storage = "6 GB LPDDR4X", "128 GB uMCP"
        elif any(x in clean for x in ["2A2", "2A"]):
            ram, storage = "8 GB LPDDR5", "256 GB uMCP"

    elif clean.startswith("KM"):
        brand = "SAMSUNG"
        if "60014BM" in clean or "60014B" in clean:
            ram, storage = "4 GB LPDDR4X", "64 GB eMMC"
        elif "60014" in clean or "P600" in clean:
            ram, storage = "3 GB LPDDR3", "32 GB eMMC"
        elif "60013" in clean or "QE600" in clean:
            ram, storage = "6 GB LPDDR4X", "128 GB eMMC"
        elif "7001" in clean or "2V700" in clean:
            ram, storage = "8 GB LPDDR5", "256 GB uMCP"
        elif "7500" in clean or "F750" in clean:
            ram, storage = "2 GB LPDDR3", "16 GB eMMC"

    elif clean.startswith(("JZ", "NW", "MT")):
        brand = "MICRON"
        if "150" in clean: ram, storage = "3 GB LPDDR3", "32 GB eMMC"
        elif "813" in clean: ram, storage = "4 GB LPDDR4X", "64 GB eMMC"
        elif "814" in clean: ram, storage = "6 GB LPDDR4X", "128 GB uMCP"

    if storage == "Unknown":
        match = re.search(r'(16|32|64|128|256|512)', clean)
        if match:
            st_val = match.group()
            storage = f"{st_val} GB"
            ram_map = {"16": "2 GB", "32": "3 GB", "64": "4 GB", "128": "6 GB", "256": "8 GB"}
            ram = ram_map.get(st_val, "Standard RAM")

    return brand, ram, storage

# 6. User Input & Button
user_input = st.text_input("IC PART NUMBER DALEIN:", placeholder="e.g. H9TQ26ADFTAC, KMRP60014M...")
click_search = st.button("🔍 DECODE IC SPECS NOW")

# 7. Native Result UI (No Raw Code Bugs)
if click_search or user_input:
    if user_input.strip():
        brand, ram, storage = master_decode_ic(user_input)
        
        st.divider()
        
        # Brand Highlight
        st.subheader(f"🏷️ BRAND: {brand}")
        
        # Clean Metric Cards
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="⚡ RAM CAPACITY", value=ram)
        with col2:
            st.metric(label="💾 INTERNAL STORAGE", value=storage)
    else:
        st.warning("कृपया पहले IC पार्ट कोड टाइप करें!")