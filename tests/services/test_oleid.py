from app.services.oleid import OleID


def test_encrypted_docx(encrypted_docx: bytes):
    oid = OleID(encrypted_docx)

    assert oid.is_encrypted() is True
    assert oid.has_flash_objects() is False
    assert oid.has_vba_macros() is False


def test_xls_with_macro(xls_with_macro: bytes):
    oid = OleID(xls_with_macro)

    assert oid.is_encrypted() is True
    assert oid.has_flash_objects() is False
    assert oid.has_vba_macros() is True
