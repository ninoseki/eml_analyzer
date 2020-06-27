import oletools.oleid
from olefile import OleFileIO, isOleFile


class OleID:
    def __init__(self, data: bytes):
        self.indicators = []

        if isOleFile(data):
            ole_file = OleFileIO(data)
            oid = oletools.oleid.OleID(ole_file)

            oid.check_encrypted()
            oid.check_excel()
            oid.check_flash()
            oid.check_word()

            self.indicators = oid.indicators

    def is_encrypted(self) -> bool:
        encrypted = [
            indicator
            for indicator in self.indicators
            if indicator.id == "encrypted" and indicator.value is True
        ]
        return len(encrypted) > 0

    def has_vba_macros(self) -> bool:
        vba_macros = [
            indicator
            for indicator in self.indicators
            if indicator.id == "vba_macros" and indicator.value is True
        ]
        return len(vba_macros) > 0

    def has_flash_objects(self) -> bool:
        flashes = [
            indicator
            for indicator in self.indicators
            if indicator.id == "flash" and indicator.value > 0
        ]
        return len(flashes) > 0
