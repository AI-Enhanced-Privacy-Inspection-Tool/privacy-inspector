def is_empty_value(value):
    """
    Helper function to determine if a value is considered "empty" for the purposes of detection.
    We treat None, empty strings, empty dicts, and empty lists as empty values.
    """
    return value is None or value == "" or value == {} or value == []