from pathlib import Path
from .app_identification import identify_app_from_path

SENSITIVE_EXTENSIONS = {
    ".sqlite", 
    ".db", 
    ".json", 
    ".log", 
    ".txt"
}

MAX_FILE_SIZE = 1_000_000  # 1 MB

def find_candidate_files_for_scanning(appdata_dirs):
    """
    Scans the given application data directories for files that are likely to contain privacy-relevant information and are safe to scan.
    Args:
        appdata_dirs: A list of directories to scan for candidate files.
    Returns:        
        A list of file paths that are candidates for scanning.
    """

    print("Finding candidate files for scanning...")
    candidates = []

    for dir in appdata_dirs:
        base_path = Path(dir)
        if not base_path.exists():
            continue

        # look through all files in the directory and its subdirectories
        for path in base_path.rglob("*"):
            # if it's a file with a sensitive extension and size is under the limit, add to candidates
            if (
                path.is_file()
                and path.suffix.lower() in SENSITIVE_EXTENSIONS
                and path.stat().st_size <= MAX_FILE_SIZE
            ):
                app_name = identify_app_from_path(path)
                candidates.append({
                    "path": path,
                    "app_name": app_name
                })

    return candidates

def classify_file(path: str) -> str:
    """
    Classifies a file based on its extension.
    Args:
        path: The path to the file to classify.
    Returns:
        A string representing the file type.
    """

    extension = Path(path).suffix.lower()

    if extension in {".sqlite", ".db", ".sqlite3"}:
        return "sqlite"
    elif extension == ".json":
        return "json"
    elif extension == ".xml": # not currently in SENSITIVE_EXTENSIONS but added for completeness
        return "xml"
    elif extension in {".txt", ".log"}:
        return "text"
    else:
        return "other"
    