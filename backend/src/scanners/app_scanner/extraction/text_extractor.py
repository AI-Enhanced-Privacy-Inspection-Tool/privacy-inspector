from pathlib import Path

from ..detection.string_detection.string_detector import detect_string_type

def walk_text(file_obj, findings, seen=None):
    """
    Walk through a text file line by line and detect privacy-relevant strings.
    Args:
        file_obj: An open file object for the text file.
        findings: A list where results are stored.
    """
    if seen is None:
        seen = set()

    for line_num, line in enumerate(file_obj, start=1):
        line = line.strip()
        if not line:
            continue

        match = detect_string_type(line)

        if match:
            record = line
            if record not in seen:
                seen.add(record)
                findings.append({
                    "field_path": f"line[{line_num}]",
                    "value_preview": line[:100],
                    **match
                })

def scan_text_file(path):
    """
    Scans a text file for privacy-relevant information and returns a list of findings.
    Args:
        path: The path to the text file to scan.
    Returns:
        A list of findings, where each finding is a dictionary containing information about a privacy-relevant value found in the text file.
    """

    findings = []

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            walk_text(f, findings)

        abs_path = str(Path(path).resolve())

        for finding in findings:
            if "file_path" not in finding:
                finding["file_path"] = abs_path
    
    except (PermissionError, OSError):
        return findings

    except Exception as e:
        print(f"[ERROR] Failed scanning text file {path}: {e}")
        return findings

    return findings