from app.services.extractor import parse_urls_from_body


def test_parse_urls_from_body_with_html(test_html: str):
    urls = parse_urls_from_body(test_html, "text/html")

    assert len(urls) > 0
    assert "http://www.w3.org/TR/html4/loose.dtd" not in urls

    # check whether urls are unique or not
    assert len(set(urls)) == len(urls)


def test_parse_urls_from_body_with_text():
    urls = parse_urls_from_body("[http://example.com]", "text/plain")
    assert len(urls) == 1
    assert "http://example.com" in urls

    urls = parse_urls_from_body("<http://example.com>", "text/plain")
    assert len(urls) == 1
    assert "http://example.com" in urls

    urls = parse_urls_from_body(
        "<http://example.com> [http://example.com]", "text/plain"
    )
    assert len(urls) == 1
    assert "http://example.com" in urls
