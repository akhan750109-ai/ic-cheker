import re
from pathlib import Path
from typing import Optional

import easyocr
import pandas as pd
import streamlit as st
from PIL import Image

DATABASE_PATH = Path(__file__).parent / "database.csv"

# Typical PCB / IC markings: MT6761V, CX90B8CAM, SM-A125F, etc.
CODE_PATTERN = re.compile(r"[A-Z0-9][A-Z0-9\-]{3,15}", re.IGNORECASE)


@st.cache_data
def load_database() -> pd.DataFrame:
    if not DATABASE_PATH.exists():
        return pd.DataFrame(columns=["Code", "CPU", "RAM_ROM", "Grade"])
    df = pd.read_csv(DATABASE_PATH, dtype=str, on_bad_lines="skip")
    df["Code"] = df["Code"].str.strip().str.upper()
    return df


@st.cache_resource
def get_ocr_reader():
    return easyocr.Reader(["en"], gpu=False)


def normalize_code(code: str) -> str:
    return code.strip().upper()


def find_match(query: str, database: pd.DataFrame) -> Optional[pd.DataFrame]:
    if not query or database.empty:
        return None

    normalized = normalize_code(query)
    exact = database[database["Code"] == normalized]
    if not exact.empty:
        return exact.iloc[[0]]

    partial = database[database["Code"].str.contains(normalized, regex=False, na=False)]
    if not partial.empty:
        return partial.iloc[[0]]

    return None


def extract_codes_from_text(texts: list[tuple]) -> list[str]:
    seen = set()
    codes = []
    for _, text, _ in texts:
        for token in CODE_PATTERN.findall(text.upper()):
            token = token.upper()
            if len(token) >= 4 and token not in seen:
                seen.add(token)
                codes.append(token)
    return codes


def display_match(result: pd.DataFrame, matched_code: str):
    row = result.iloc[0]
    st.success(f"Match found for **{matched_code}**")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Code", row["Code"])
        st.metric("CPU", row["CPU"])
    with col2:
        st.metric("RAM / ROM", row["RAM_ROM"])
        st.metric("Grade", row["Grade"])


def run_lookup(query: str, database: pd.DataFrame, source_label: str):
    if not query:
        st.warning("Please enter or upload a code to search.")
        return

    match = find_match(query, database)
    if match is not None:
        display_match(match, query)
    else:
        st.error(f"❌ '{query}' डेटाबेस में नहीं मिला।")

def main():
    st.set_page_config(page_title="Mobile Scrap PCB Identifier", page_icon="🔍", layout="wide")
    st.title("Mobile Scrap PCB Identifier")
    st.caption("Upload a PCB photo or type a code to look up CPU, RAM/ROM, and grade.")

    database = load_database()
    if database.empty:
        st.error(f"Database not found or empty. Expected file: {DATABASE_PATH}")
        st.stop()

    tab_photo, tab_manual = st.tabs(["Photo Upload", "Manual Code Search"])

    with tab_photo:
        st.subheader("Upload PCB Photo")
        st.write("Upload a clear photo of the PCB. EasyOCR will scan printed codes on the board.")

        uploaded = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp", "bmp"])

        if uploaded is not None:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded PCB image", use_container_width=True)

            with st.spinner("Running OCR — first run may download models (~100 MB)..."):
                import numpy as np

                reader = get_ocr_reader()
                results = reader.readtext(np.array(image))

            if not results:
                st.warning("No text detected in the image. Try a clearer, well-lit photo.")
            else:
                extracted_codes = extract_codes_from_text(results)

                with st.expander("All OCR text detected"):
                    for bbox, text, confidence in results:
                        st.write(f"**{text}** (confidence: {confidence:.0%})")

                if not extracted_codes:
                    st.warning("Text was found but no PCB-style codes were recognized.")
                else:
                    st.write("**Extracted codes:**")
                    selected = st.selectbox(
                        "Select a code to look up",
                        extracted_codes,
                        key="ocr_code_select",
                    )

                    if st.button("Look up selected code", key="ocr_lookup_btn"):
                        run_lookup(selected, database, "OCR")

                    st.divider()
                    st.write("**Quick lookup for all extracted codes:**")
                    for code in extracted_codes:
                        match = find_match(code, database)
                        if match is not None:
                            with st.container(border=True):
                                display_match(match, code)
                        else:
                            st.caption(f"{code} — no database match")

    with tab_manual:
        st.subheader("Manual Code Search")
        st.write("Type a motherboard or IC code printed on the PCB.")

        manual_code = st.text_input(
            "Enter code",
            placeholder="e.g. MT6761V or CX90B8CAM",
            key="manual_code_input",
        ).strip()

        if st.button("Search", key="manual_search_btn"):
            run_lookup(manual_code, database, "manual entry")


if __name__ == "__main__":
    main()
