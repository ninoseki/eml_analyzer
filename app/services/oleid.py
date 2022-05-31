from typing import Any, Optional

import oletools.oleid
from olefile import isOleFile


def is_truthy(v: Any) -> bool:
    if v is None:
        return False

    if isinstance(v, bool):
        return v is True

    if isinstance(v, int):
        return v > 0

    try:
        return str(v).upper() == "YES"
    except Exception:
        return False


class OleID:
    def __init__(self, data: bytes):
        self.oid: Optional[oletools.oleid.OleID] = None

        if isOleFile(data):
            self.oid = oletools.oleid.OleID(data=data)
            self.oid.check()

    def is_encrypted(self) -> bool:
        if self.oid is None:
            return False

        encrypted = self.oid.get_indicator("encrypted")
        return is_truthy(encrypted.value)

    def has_vba_macros(self) -> bool:
        if self.oid is None:
            return False

        macros = self.oid.get_indicator("vba")
        return is_truthy(macros.value)

    def has_xlm_macros(self) -> bool:
        if self.oid is None:
            return False

        macros = self.oid.get_indicator("xlm")
        return is_truthy(macros.value)

    def has_flash_objects(self) -> bool:
        if self.oid is None:
            return False

        flash = self.oid.get_indicator("flash")
        return is_truthy(flash.value)

    def has_external_relationships(self) -> bool:
        if self.oid is None:
            return False

        flash = self.oid.get_indicator("ext_rels")
        return is_truthy(flash.value)

    def has_object_pool(self) -> bool:
        if self.oid is None:
            return False

        flash = self.oid.get_indicator("ObjectPool")
        return is_truthy(flash.value)
