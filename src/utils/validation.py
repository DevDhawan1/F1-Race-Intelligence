def require_columns(frame, required_columns):
    """Raise a clear error when an analysis input lacks required columns."""
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")
