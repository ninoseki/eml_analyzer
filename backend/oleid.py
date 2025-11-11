import oletools.oleid
from olefile import isOleFile

from backend.utils import is_truthy


class OleID:
    def __init__(self, data: bytes):
        self.oid: oletools.oleid.OleID | None = None

        if isOleFile(data):
            self.oid = oletools.oleid.OleID(data=data)
            self.oid.check()

    def _is_truthy_by_indicator_id(self, indicator_id: str) -> bool:
        if self.oid:
            indicator = self.oid.get_indicator(indicator_id)
            if indicator:
                return is_truthy(indicator.value)

        return False

    @property
    def has_encrypted(self) -> bool:
        return self._is_truthy_by_indicator_id("encrypted")

    @property
    def has_vba_macros(self) -> bool:
        return self._is_truthy_by_indicator_id("vba")

    @property
    def has_xlm_macros(self) -> bool:
        return self._is_truthy_by_indicator_id("xlm")

    @property
    def has_flash_objects(self) -> bool:
        return self._is_truthy_by_indicator_id("flash")

    @property
    def has_external_relationships(self) -> bool:
        return self._is_truthy_by_indicator_id("ext_rels")

    @property
    def has_object_pool(self) -> bool:
        return self._is_truthy_by_indicator_id("ObjectPool")
