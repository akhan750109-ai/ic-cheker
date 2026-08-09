# Mobile Scrap PCB Identifier

A free Python Streamlit app to identify mobile scrap PCBs by matching printed codes against a local CSV database.

## Features

- **Photo Upload** — Upload a PCB image; EasyOCR extracts printed codes (e.g. MT6761V, CX90B8CAM).
- **Manual Code Search** — Type a motherboard or IC code directly.
- **Local database** — Matches against `database.csv` (Code, CPU, RAM_ROM, Grade).

## Setup

```bash
pip install -r requirements.txt
```

First OCR run downloads EasyOCR models (~100 MB). No API keys required.

## Run

```bash
streamlit run app.py
```

## Database

Edit `database.csv` to add your own PCB codes:

| Code       | CPU                  | RAM_ROM  | Grade |
|------------|----------------------|----------|-------|
| MT6761V    | MediaTek Helio A22   | 2GB/32GB | A     |
| CX90B8CAM  | Snapdragon 662       | 4GB/64GB | B     |
| SM-A125F   | Exynos 850           | 4GB/64GB | B     |
| MT6765G    | MediaTek Helio P35   | 3GB/32GB | C     |
