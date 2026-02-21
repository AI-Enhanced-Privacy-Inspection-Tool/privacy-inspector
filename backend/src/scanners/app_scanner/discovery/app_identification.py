from pathlib import Path

def identify_app_from_path(file_path: Path) -> str:
    # if on Windows
    parts = file_path.parts

    try:
        if "Roaming" in parts:
            idx = parts.index("Roaming")
            return parts[idx + 1]
        elif "Local" in parts:
            idx = parts.index("Local")
            return parts[idx + 1]
    except (ValueError, IndexError):
        pass

    return "Unknown"

    # TODO: add the funcionality for other operating systems