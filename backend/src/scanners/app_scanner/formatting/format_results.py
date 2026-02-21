from collections import defaultdict

def format_results(all_findings):
    """
    Build compact detailed results:
    - Each app appears once
    - Each category appears once per app
    - Keeps first file_path + value_preview found
    """

    apps = defaultdict(dict)

    for finding in all_findings:
        app = finding["app_name"]
        category = finding["category"]

        if category not in apps[app]:
            apps[app][category] = {
                "file_path": finding["file_path"],
                "value_preview": finding["value_preview"],
                "field_path": finding["field_path"],
                "detection_method": finding["detection_method"],
                "confidence": finding["confidence"]
            }

    return {
        "apps": {
            app: [
                {
                    "value_preview": info["value_preview"],
                    "category": category,
                    "file_path": info["file_path"],
                    "field_path": info["field_path"],
                    "detection_method": info["detection_method"],
                    "confidence": info["confidence"]
                }
                for category, info in categories.items()
            ]
            for app, categories in apps.items()
        }
    }