from collections import defaultdict

def compact_results(findings):
    """
    Build compact results:
    - Each app appears once
    - Each category appears once per app
    """

    results = defaultdict(set)

    for finding in findings:
        app_name = finding["app_name"].lower()
        category = finding["category"]
        results[app_name].add(category)

    return {
        app: sorted(list(categories))
        for app, categories in results.items()
    }