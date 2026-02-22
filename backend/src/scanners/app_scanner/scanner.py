import logging
from collections import Counter, defaultdict
from tqdm import tqdm

from .discovery.app_data_locations import get_app_data_dirs
from .discovery.file_discovery import classify_file, find_candidate_files_for_scanning
from .extraction.json_extractor import scan_json_file
from .extraction.sqlite_extractor import scan_sqlite_file
from .extraction.text_extractor import scan_text_file
from .formatting.format_results import format_results
from .formatting.compact_results import compact_results

logger = logging.getLogger(__name__)

def scan_app_files(filter_category=None):
    """
    Scan candidate files and return findings.

    Args:
        filter_category (str | None):
            If provided, only findings matching this category are returned.
    """

    logger.info("Starting scan...")
    appdata_dirs = get_app_data_dirs()
    candidate_files = find_candidate_files_for_scanning(appdata_dirs)
    logger.info(f"Scanning {len(candidate_files)} files...")

    counts = Counter()
    all_findings = []
    results = defaultdict(set)

    for file_info in tqdm(candidate_files, desc="Scanning files", unit="file", total=len(candidate_files)):
        path = file_info["path"]
        app_name = file_info["app_name"].lower()

        file_type = classify_file(path)
        counts[file_type] += 1

        if file_type == "json":
            findings = scan_json_file(path)
        elif file_type == "text":
            findings = scan_text_file(path)
        #if file_type == "sqlite":
          #  findings = scan_sqlite_file(path)

        for finding in findings:
            if filter_category and finding["category"] != filter_category:
                continue

            finding["file_path"] = str(path)
            finding["app_name"] = app_name
            all_findings.append(finding)
            results[app_name].add(finding["category"])
    
    logger.info(f"Scan complete: {len(all_findings)} findings from {len(results)} apps")
    compacted_results = compact_results(all_findings)
    formatted_results = format_results(all_findings)

    return counts, all_findings, compacted_results, formatted_results