 import streamlit as st
import re

# 1. Page Config
st.set_page_config(
    page_title="PRO IC DECODER", 
    page_icon="⚡", 
    layout="centered"
)

# 2. Modern UI CSS Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        font-family: 'Segoe UI', Roboto, sans-serif;
    }
    
    .main-title {
        font-size: 40px !important;
        font-weight: 900 !important;
        text-align: center;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    
    .sub-title {
        font-size: 15px;
        text-align: center;
        color: #94a3b8;
        margin-bottom: 25px;
        font-weight: 500;
    }

    .stTextInput label {
        color: #38bdf8 !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        letter-spacing: 1px;
    }
    .stTextInput input {
        font-size: 22px !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.2);
        text-transform: uppercase;
    }
    .stTextInput input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 25px rgba(129, 140, 248, 0.5) !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown('<div class="main-title">⚡ IC SPEC FINDER PRO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instant Smart Chip Specs Decoder for Mobile Repairing</div>', unsafe_allow_html=True)

# 4. Master Exact Database
EXACT_IC_DB = {
    # SK Hynix
    "H9TQ15ADFTMC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ16ADFTMC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ17ABJTAC": ("2 GB LPDDR3", "16 GB eMMC", "SK HYNIX"),
    "H9TQ26ADFTAC": ("3 GB LPDDR3", "32 GB eMMC", "SK HYNIX"),
    "H9TQ65ACRNAC": ("4 GB LPDDR3", "64 GB eMMC", "SK HYNIX"),
    "H54T1A20AFR": ("6 GB LPDDR4X", "128 GB uMCP", "SK HYNIX"),
    "H58T52ACACR": ("4 GB LPDDR4X", "64 GB uMCP", "SK HYNIX"),
    "H58T27ACACR": ("8 GB LPDDR4X", "256 GB uMCP", "SK HYNIX"),

    # Samsung
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

    # Micron & Others
    "JZ150": ("3 GB LPDDR3", "32 GB eMMC", "MICRON"),
    "NW813": ("4 GB LPDDR4X", "64 GB eMMC", "MICRON"),
    "NW814": ("6 GB LPDDR4X", "128 GB uMCP", "MICRON"),
    "SDINADF4128G": ("No RAM", "128 GB eMMC", "SANDISK"),
    "SDINBDG464G": ("No RAM", "64 GB eMMC", "SANDISK")
}

# 5. Hybrid Decoder Engine
def master_decode_ic(code):
    clean = code.upper().replace("-", "").strip()
    if not clean:
        return None, None, None

    # Layer 1: Direct Master DB Match
    if clean in EXACT_IC_DB:
        ram, storage, brand = EXACT_IC_DB[clean]
        return brand, ram, storage

    # Sub-string DB Search
    for key in EXACT_IC_DB:
        if key in clean or clean in key:
            ram, storage, brand = EXACT_IC_DB[key]
            return brand, ram, storage

    brand = "GENERIC / UNKNOWN"
    ram = "Unknown"
    storage = "Unknown"

    # Layer 2: Rule-Based Logic
    # --- SK HYNIX ---
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

    # --- SAMSUNG ---
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

    # --- MICRON ---
    elif clean.startswith(("JZ", "NW", "MT")):
        brand = "MICRON"
        if "150" in clean: ram, storage = "3 GB LPDDR3", "32 GB eMMC"
        elif "813" in clean: ram, storage = "4 GB LPDDR4X", "64 GB eMMC"
        elif "814" in clean: ram, storage = "6 GB LPDDR4X", "128 GB uMCP"

    # Layer 3: Fallback Regex for Unseen Codes
    if storage == "Unknown":
        match = re.search(r'(16|32|64|128|256|512)', clean)
        if match:
            st_val = match.group()
            storage = f"{st_val} GB"
            ram_map = {"16": "2 GB", "32": "3 GB", "64": "4 GB", "128": "6 GB", "256": "8 GB"}
            ram = ram_map.get(st_val, "Standard RAM")

    return brand, ram, storage

# 6. User Input Section
user_input = st.text_input("ENTER IC PART CODE:", placeholder="e.g. H9TQ15ADFTMC, KMRP60014M...")

# 7. UI Display Card
if user_input:
    brand, ram, storage = master_decode_ic(user_input)
    
    result_card = f"""
    <div style="
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(10px);
        border: 2px solid #818cf8;
        border-radius: 16px;
        padding: 25px;
        margin-top: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(129, 140, 248, 0.2);
    ">
        <div style="text-align: center; margin-bottom: 20px;">
            <span style="
                background: linear-gradient(90deg, #0284c7, #3b82f6);
                color: #ffffff;
                font-size: 14px;
                font-weight: 800;
                padding: 6px 16px;
                border-radius: 20px;
                letter-spacing: 1.5px;
            ">BRAND: {brand}</span>
            <h2 style="
                color: #38bdf8;
                font-size: 28px;
                font-weight: 800;
                margin: 15px 0 5px 0;
                letter-spacing: 1px;
            ">{user_input.upper()}</h2>
        </div>

        <div style="
            display: flex;
            justify-content: space-around;
            background: rgba(15, 23, 42, 0.6);
            border-radius: 12px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        ">
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 14px; font-weight: 700; margin-bottom: 5px;">⚡ RAM CAPACITY</div>
                <div style="color: #fde047; font-size: 26px; font-weight: 900;">{ram}</div>
            </div>
            <div style="border-left: 1px solid #334155;"></div>
            <div style="text-align: center;">
                <div style="color: #94a3b8; font-size: 14px; font-weight: 700; margin-bottom: 5px;">💾 INTERNAL STORAGE</div>
                <div style="color: #4ade80; font-size: 26px; font-weight: 900;">{storage}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(result_card, unsafe_allow_html=True)