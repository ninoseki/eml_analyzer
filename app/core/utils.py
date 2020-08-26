from starlette.datastructures import Secret

import app.core.settings


def is_secret(value) -> bool:
    return isinstance(value, Secret)


def has_urlscan_api_key() -> bool:
    return (
        is_secret(app.core.settings.URLSCAN_API_KEY)
        and str(app.core.settings.URLSCAN_API_KEY) != ""
    )


def has_virustotal_api_key() -> bool:
    return (
        is_secret(app.core.settings.VIRUSTOTAL_API_KEY)
        and str(app.core.settings.VIRUSTOTAL_API_KEY) != ""
    )


def has_inquest_api_key() -> bool:
    return (
        is_secret(app.core.settings.INQUEST_API_KEY)
        and str(app.core.settings.INQUEST_API_KEY) != ""
    )
