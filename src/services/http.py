import requests
import fastf1._api


_configured = False
_original_session_request = requests.Session.request


def _request_with_default_timeout(self, method, url, **kwargs):
    if "timeout" not in kwargs or kwargs["timeout"] is None:
        kwargs["timeout"] = (10, 60)
    return _original_session_request(self, method, url, **kwargs)


def configure_http():
    """Apply shared HTTP defaults once for FastF1 and external services."""
    global _configured
    if _configured:
        return
    requests.Session.request = _request_with_default_timeout
    fastf1._api.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.formula1.com/",
        "Origin": "https://www.formula1.com",
    })
    _configured = True
