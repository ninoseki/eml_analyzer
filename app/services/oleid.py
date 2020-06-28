import oletools.oleid
from olefile import OleFileIO, isOleFile


class OleID:
    def __init__(self, data: bytes):
        if isOleFile(data):
            ole_file = OleFileIO(data)
            self.oid = oletools.oleid.OleID(ole_file)
            self.oid.check()

    def is_encrypted(self) -> bool:
        encrypted = self.oid.get_indicator("encrypted")
        return encrypted is not None and encrypted.value is True

    def has_vba_macros(self) -> bool:
        macros = self.oid.get_indicator("vba_macros")
        return macros is not None and macros.value is True

    def has_flash_objects(self) -> bool:
        flash = self.oid.get_indicator("flash")
        return flash is not None and flash.value > 0
