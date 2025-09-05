from email.message import EmailMessage
from typing import BinaryIO

from compoundfiles import CompoundFileReader
from outlookmsgfile import load_message_stream


class Message:
    def __init__(self, filename_or_stream: str | BinaryIO):
        self.filename_or_stream = filename_or_stream

    def to_email(self) -> EmailMessage:
        with CompoundFileReader(self.filename_or_stream) as doc:
            doc.rtf_attachments = 0
            return load_message_stream(doc.root, True, doc)
