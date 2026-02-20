import json
import sys
from pathlib import Path

# for running this file directly as `python main.py` from inside the `app_scanner` folder
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app_scanner.scanner import scan_app_files

def main():
    counts, findings, compact_results = scan_app_files()

    print("Candidate files by format:")
    for file_type, count in counts.items():
        print(f"{count} {file_type} files found")

    print(f"\nTotal findings: {len(findings)}\n")

    for finding in findings[:20]:
        print(finding)

    print("\nCompact Results by App:\n")

    json_compact_results = json.dumps(compact_results, indent=4)
    print(json_compact_results)
    
def test():
    counts, phone_findings = scan_app_files(filter_category="ipaddress")

    print("Candidate files by format:")
    for file_type, count in counts.items():
        print(f"{count} {file_type} files found")

    print(f"\nTotal phone number findings: {len(phone_findings)}\n")

    for finding in phone_findings[:20]:
        print(finding)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test() # python main.py test
    else:
        main() # python main.py 