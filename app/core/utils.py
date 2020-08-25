from app.core.settings import INQUEST_API_KEY, URLSCAN_API_KEY, VIRUSTOTAL_API_KEY


def has_urlscan_api_key() -> bool:
    return str(URLSCAN_API_KEY) != ""


def has_virustotal_api_key() -> bool:
    return str(VIRUSTOTAL_API_KEY) != ""


def has_inquest_api_key() -> bool:
    return str(INQUEST_API_KEY) != ""
