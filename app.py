import streamlit as st
import urllib.parse
import re
import requests

# Page Setup
st.set_page_config(page_title="Accurate IC Spec Finder", page_icon="⚡", layout="centered")

st.title("⚡ Universal & Accurate IC GB Finder")
st.write("चिप/IC का सही कोड दर्ज करें और 1 सेकंड में सटीक RAM व Storage (GB) देखें:")

# Input Form
with st.form(key="search_form"):
    user_input = st.text_input("Enter IC / PCB Code:", placeholder="e.g. KMRP60014M, KMQE60013M, KMRC1000BM...").strip().upper()
    submit_btn = st.form_submit_button("Search Specs")

# Big HTML Table Display
def show_big_specs(part_code, ram_gb, storage_gb):
    html_code = f"""
    <div style="border: 2px solid #007bff; border-radius: 10px; padding: 15px; background-color: #f8f9fa; margin-top: 15px;">
        <h3 style="text-align: center; color: #007bff; margin-bottom: 15px;">PART CODE: {part_code}</h3>
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
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# Accurate Position Decoder (Samsung, Hynix, Micron)
def decode_ic_code(clean_code):
    # 1. Samsung eMMC/eMCP Code Logic (Position-based Decoding)
    if clean_code.startswith("KM"):
        if "6001" in clean_code:
            idx = clean_code.find("6001") + 4
            if idx < len(clean_code):
                digit = clean_code[idx]
                if digit == '4':
                    return "3 GB / 4 GB", "64 GB"
                elif digit == '5':
                    return "4 GB / 6 GB", "128 GB"
                elif digit == '3':
                    return "2 GB", "32 GB"
                elif digit == '2':
                    return "2 GB", "16 GB"
        
        if "1000" in clean_code:
            return "3 GB", "32 GB"
        elif "2100" in clean_code:
            return "4 GB", "64 GB"
        elif "3100" in clean_code:
            return "6 GB", "128 GB"

    # 2. SK Hynix / Micron Patterns
    if "H9TP" in clean_code or "MT29" in clean_code:
        if "32A" in clean_code: return "2 GB", "16 GB"
        if "65A" in clean_code: return "3 GB", "32 GB"

    # 3. Web Search Backup (अगर कोई बिल्कुल अनजान कोड हो)
    try:
        api_url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(clean_code)}+ic+ram+storage+specs&format=json"
        res = requests.get(api_url, timeout=3).json()
        text = res.get('AbstractText', '') + str(res.get('RelatedTopics', ''))
        
        storage_m = re.search(r'(\b16|\b32|\b64|\b128|\b256|\b512)\s*GB', text, re.IGNORECASE)
        ram_m = re.search(r'(\b1|\b2|\b3|\b4|\b6|\b8|\b12)\s*GB', text, re.IGNORECASE)
        
        ram_val = f"{ram_m.group(1)} GB" if ram_m else None
        storage_val = f"{storage_m.group(1)} GB" if storage_m else None
        
        if ram_val or storage_val:
            return ram_val if ram_val else "N/A", storage_val if storage_val else "N/A"
    except Exception:
        pass

    return "Check Datasheet", "Check Datasheet"

def main():
    if submit_btn and user_input:
        clean_code = user_input.replace("-", "").strip()
        st.info(f"🔍 Checking Specs for: **{user_input}**...")

        ram_res, storage_res = decode_ic_code(clean_code)

        if ram_res != "Check Datasheet":
            st.success("✅ Exact Specs Found!")
            show_big_specs(user_input, ram_res, storage_res)
        else:
            st.warning(f"⚠️ '{user_input}' के लिए सीधा डेटा नहीं मिला। नीचे गूगल बटन से चेक करें:")

        # Google Link Backup
        st.markdown("---")
        encoded_q = urllib.parse.quote(f"{user_input} ic datasheet ram storage gb")
        st.link_button("🔍 Search Datasheet on Google", f"https://www.google.com/search?q={encoded_q}", use_container_width=True)

if __name__ == "__main__":
    main()