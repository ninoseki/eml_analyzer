from typing import Optional

import oletools.oleid
from olefile import OleFileIO, isOleFile


class OleID:
    def __init__(self, data: bytes):
        self.oid: Optional[oletools.oleid.OleID] = None

        if isOleFile(data):
            ole_file = OleFileIO(data)
            self.oid = oletools.oleid.OleID(ole_file)
            self.oid.check()

    def is_encrypted(self) -> bool:
        if self.oid is None:
            return False

        encrypted = self.oid.get_indicator("encrypted")
        return encrypted is not None and encrypted.value is True

    def has_vba_macros(self) -> bool:
        if self.oid is None:
            return False

        macros = self.oid.get_indicator("vba_macros")
        return macros is not None and macros.value is True

    def has_flash_objects(self) -> bool:
        if self.oid is None:
            return False

        flash = self.oid.get_indicator("flash")
        return flash is not None and flash.value > 0
