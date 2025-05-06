def validate_query(query: str) -> list:
    """Check for common terminology mismatches"""
    warnings = []
    
    term_map = {
        'host': 'server_id',
        'machine': 'server_id',
        '%': 'metric_value',
        'time': 'timestamp'
    }
    
    for wrong_term, correct_term in term_map.items():
        if wrong_term in query.lower():
            warnings.append(f"• Using '{correct_term}' instead of '{wrong_term}'")
    
    return warnings