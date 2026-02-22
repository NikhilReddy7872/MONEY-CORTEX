def validate_query(sql: str) -> bool:
    sql = sql.strip().lower()

    # Only allow SELECT
    if not sql.startswith("select"):
        return False

    # Block multiple statements
    if ";" in sql:
        return False

    return True