import pytest

from backend.utils import normalize_url, parse_urls_from_body


@pytest.mark.parametrize(
    ("url", "expected"),
    [
        ("https://example.com", "https://example.com"),
        ("https://example.com>", "https://example.com"),
        ("https://example.com>>", "https://example.com"),
        ("https://example.com]", "https://example.com"),
        ("https://example.com]]", "https://example.com"),
        ("https://example.com>]", "https://example.com"),
        ("https://example.com/path?q=1>", "https://example.com/path?q=1"),
    ],
)
def test_normalize_url(url: str, expected: str):
    assert normalize_url(url) == expected


@pytest.mark.parametrize(
    ("content", "content_type", "expected"),
    [
        # plain text with a URL
        (
            "Visit https://example.com for details.",
            "text/plain",
            {"https://example.com"},
        ),
        # plain text with multiple URLs
        (
            "See https://a.com and https://b.com",
            "text/plain",
            {"https://a.com", "https://b.com"},
        ),
        # no URLs
        ("no links here", "text/plain", set()),
        # HTML href extraction
        (
            '<a href="https://example.com">link</a>',
            "text/html",
            {"https://example.com"},
        ),
        # HTML with URL in text (not in href)
        (
            "<p>Visit https://example.com</p>",
            "text/html",
            {"https://example.com"},
        ),
        # HTML with both href and text URLs
        (
            '<a href="https://a.com">https://b.com</a>',
            "text/html",
            {"https://a.com", "https://b.com"},
        ),
        # non-http hrefs are excluded
        (
            '<a href="mailto:a@b.com">email</a>',
            "text/html",
            set(),
        ),
    ],
)
def test_parse_urls_from_body(content: str, content_type: str, expected: set[str]):
    assert parse_urls_from_body(content, content_type) == expected
