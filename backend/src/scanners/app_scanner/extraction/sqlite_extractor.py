import sqlite3
from pathlib import Path
from ..detection.patterns import PRIVACY_CATEGORIES
from ..detection.string_detection.string_detector import detect_string_type

def walk_sqlite(conn, findings, seen=None):
    """
    Walk through all tables and columns in the SQLite DB and detect privacy-relevant strings.
    Args:
        conn: An active connection to the SQLite database.
        findings: A list where results are stored.
    """
    if seen is None:
        seen = set()

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for (table_name,) in tables:
        try:
            cursor.execute(f"SELECT * FROM `{table_name}` LIMIT 1000;")  # limit to avoid huge tables
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            print(f"Columns found: {columns} in table {table_name}")

            for row_index, row_content in enumerate(rows):
                for col_index, col_value in enumerate(row_content):
                    if col_value is None or col_value == "" or col_value == {} or col_value == []:
                        continue

                    col_value_str = str(col_value)

                    # value based detection
                    match = detect_string_type(col_value_str)
                    if match:
                        record = col_value_str
                        if record not in seen:
                            seen.add(record)
                            findings.append({
                                "field_path": f"{table_name}.{columns[col_index]}[{row_index}]",
                                "value_preview": col_value_str[:100],
                                **match
                            })
                        continue  # if we found a value-based match, we can skip key-based detection for this cell
                    
                    # if no value-based match, try key-based detection using the column name
                    for category in PRIVACY_CATEGORIES:
                        if category == columns[col_index].lower():
                            record = col_value_str
                            if record not in seen:
                                seen.add(record)
                                findings.append({
                                    "field_path": f"{table_name}.{columns[col_index]}[{row_index}]",
                                    "value_preview": col_value_str[:100],
                                    "category": category,
                                    "detection_method": "column_name",
                                    "confidence": "medium"
                                })

                            break  # stop checking other categories

        except Exception as e:
            print(f"[WARNING] Failed to scan table {table_name}: {e}")
            continue


def scan_sqlite_file(path):
    """
    Scans a SQLite database for privacy-relevant information and returns a list of findings.
    Args:
        path: The path to the SQLite database file.
    Returns:
        A list of findings, where each finding is a dictionary containing details about the detected privacy-relevant data.
    """
    findings = []

    try:
        conn = sqlite3.connect(path)
        walk_sqlite(conn, findings)
        conn.close()

        abs_path = str(Path(path).resolve())
        for finding in findings:
            if "file_path" not in finding:
                finding["file_path"] = abs_path
    
    except (PermissionError, OSError):
        return findings

    except Exception as e:
        print(f"[ERROR] Failed scanning SQLite file {path}: {e}")

    return findings