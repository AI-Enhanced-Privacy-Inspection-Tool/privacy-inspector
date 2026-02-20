import json

from app_scanner.detection.empty_value_detector import is_empty_value
from ..detection.patterns import PRIVACY_CATEGORIES, normalize_key
from app_scanner.detection.string_detection.string_detector import detect_string_type

def walk_json(obj, findings, path="", seen=None):
    """
    Recursively walk through JSON data and look for values that match privacy-relevant patterns.
    Args:
        obj: The current piece of JSON data being analyzed.
        findings: A list where results are stored.
    """
    if seen is None:
        seen = set()

    # if the object is a dictionary, we check each key and value
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            normalized_key = normalize_key(key)

            # key-based detection
            for category in PRIVACY_CATEGORIES:
                if category in normalized_key:
                    if is_empty_value(value):
                        break
                     
                    record = (value)
                    # check if we've already recorded a finding for this path and category to avoid duplicates
                    if record not in seen:
                        seen.add(record)
                        findings.append({
                            "field_path": new_path,
                            "value_preview": str(value)[:100],
                            "category": category,
                            "detection_method": "key_name",
                            "confidence": "medium"
                        })
                        
                    break  # stop checking other categories if we found a match

            # if the key didn't match any category, we still want to check the value
            walk_json(value, findings, new_path, seen)

    # if the object is a list, we check each item in the list
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            walk_json(item, findings, f"{path}[{i}]", seen)

    # if the object is a string, we apply value-based detection
    # (not that needed since emails and phone numbers often will have keys that trigger key-based detection)
    elif isinstance(obj, str):
        if is_empty_value(obj):
            return

        match = detect_string_type(obj)

        if match:
            record = obj
            if record not in seen:
                seen.add(record)
                findings.append({
                    "field_path": path,
                    "value_preview": obj[:100],
                    **match
                })

def scan_json_file(path):
    """
    Scans a JSON file for privacy-relevant information and returns a list of findings.
    Args:
        path: The path to the JSON file to scan.
    Returns:
        A list of findings, where each finding is a dictionary containing information about a privacy-relevant value found in the JSON.
    """
    findings = []

    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)

        walk_json(data, findings)

        # attach the file path to each finding so callers always know origin
        try:
            from pathlib import Path
            abs_path = str(Path(path).resolve())
        except Exception:
            abs_path = str(path)

        for finding in findings:
            # do not overwrite if caller already set `file_path`
            if "file_path" not in finding:
                finding["file_path"] = abs_path

    except Exception as e:
        print(f"[ERROR] Failed scanning JSON file {path}: {e}")

    return findings