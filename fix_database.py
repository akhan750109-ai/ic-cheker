"""Repair database.csv: split fused rows and deduplicate conflicting codes."""

import csv
import re
from collections import defaultdict
from pathlib import Path

SOURCE = Path(r"c:\Users\akhan\Downloads\database.csv")
OUTPUT = Path(__file__).parent / "database.csv"

CODE_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-]{2,20}$", re.IGNORECASE)
GRADE_RE = re.compile(r"^[A-D]$")


def looks_like_code(value: str) -> bool:
    return bool(CODE_RE.match(value.strip()))


def parse_fused_fields(fields: list[str]) -> list[tuple[str, str, str, str]]:
    """Split extra comma-separated fields into valid 4-column records."""
    records: list[tuple[str, str, str, str]] = []
    i = 0
    while i < len(fields):
        if i + 3 >= len(fields):
            break

        code, cpu, ram_rom = fields[i], fields[i + 1], fields[i + 2]
        fourth = fields[i + 3]

        if GRADE_RE.match(fourth):
            records.append((code, cpu, ram_rom, fourth))
            i += 4
            continue

        if looks_like_code(fourth):
            # Missing grade before the next code; infer from RAM tier.
            grade = infer_grade(ram_rom)
            records.append((code, cpu, ram_rom, grade))
            i += 3
            continue

        # Corrupted fusion such as "SDINBDG4-…KLMCGAFE4B-B001"
        split = re.split(r"(?=KLMCGAFE4B-B001$)", fourth)
        if len(split) == 2 and split[1]:
            left = split[0].rstrip("-….")
            if left:
                records.append((left, cpu, ram_rom, infer_grade(ram_rom)))
            records.append((split[1], fields[i + 4], fields[i + 5], fields[i + 6]))
            i += 7
            continue

        grade = infer_grade(ram_rom)
        records.append((code, cpu, ram_rom, grade))
        i += 4

    return records


def infer_grade(ram_rom: str) -> str:
    ram_rom = ram_rom.upper()
    if "1GB/8GB" in ram_rom or "1GB/8" in ram_rom:
        return "D"
    if "2GB/16GB" in ram_rom or "2GB/16" in ram_rom:
        return "C"
    if "3GB/32GB" in ram_rom or "3GB/32" in ram_rom:
        return "B"
    return "A"


def load_records(path: Path) -> list[tuple[str, str, str, str]]:
    records: list[tuple[str, str, str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        if header != ["Code", "CPU", "RAM_ROM", "Grade"]:
            raise ValueError(f"Unexpected header: {header}")

        for line_no, fields in enumerate(reader, start=2):
            fields = [field.strip() for field in fields if field.strip() != ""]
            if not fields:
                continue
            if len(fields) == 4 and GRADE_RE.match(fields[3]):
                records.append(tuple(fields))  # type: ignore[arg-type]
            elif len(fields) > 4:
                records.extend(parse_fused_fields(fields))
            else:
                raise ValueError(f"Line {line_no}: cannot parse {fields!r}")

    return records


def dedupe_records(records: list[tuple[str, str, str, str]]) -> list[tuple[str, str, str, str]]:
    by_code: dict[str, list[tuple[str, str, str, str]]] = defaultdict(list)
    for record in records:
        code = record[0].upper()
        by_code[code].append(record)

    cleaned: list[tuple[str, str, str, str]] = []
    conflicts: list[str] = []

    for code in sorted(by_code.keys(), key=lambda c: records.index(by_code[c][0])):
        variants = by_code[code]
        unique = list(dict.fromkeys(variants))
        if len(unique) == 1:
            cleaned.append(unique[0])
            continue

        # Prefer the variant seen most often, then the most specific CPU label.
        scored = sorted(
            unique,
            key=lambda r: (
                sum(1 for v in variants if v == r),
                len(r[1]),
                -ord(r[3]),  # higher grade wins when tied
            ),
            reverse=True,
        )
        winner = scored[0]
        cleaned.append(winner)
        others = [v for v in unique if v != winner]
        conflicts.append(
            f"{code}: kept {winner[2]}/{winner[3]} ({winner[1]}); "
            f"dropped {[f'{o[2]}/{o[3]}' for o in others]}"
        )

    return cleaned, conflicts


def main() -> None:
    records = load_records(SOURCE)
    cleaned, conflicts = dedupe_records(records)

    with OUTPUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Code", "CPU", "RAM_ROM", "Grade"])
        writer.writerows(cleaned)

    print(f"Wrote {len(cleaned)} unique records to {OUTPUT}")
    print(f"Removed {len(records) - len(cleaned)} duplicate/conflicting rows")
    if conflicts:
        print("\nResolved conflicts:")
        for item in conflicts:
            print(f"  - {item}")


if __name__ == "__main__":
    main()
