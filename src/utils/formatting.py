def format_lap_time(seconds):
    """Convert seconds to ``M:SS.mmm`` or ``-`` for invalid values."""
    if seconds is None:
        return "-"
    try:
        seconds = float(seconds)
    except (TypeError, ValueError):
        return "-"
    if seconds != seconds:
        return "-"
    minutes = int(seconds // 60)
    remaining = seconds - (minutes * 60)
    return f"{minutes}:{remaining:06.3f}"


def format_duration(duration):
    """Convert a timedelta-like value or seconds to a readable duration."""
    if duration is None:
        return "-"
    try:
        total_seconds = int(duration.total_seconds())
    except AttributeError:
        try:
            total_seconds = int(float(duration))
        except (TypeError, ValueError):
            return "-"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours > 0:
        return f"{hours}h {minutes}m {seconds}s"
    if minutes > 0:
        return f"{minutes}m {seconds}s"
    return f"{seconds}s"
