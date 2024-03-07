# Forked from https://github.com/JoshData/convert-outlook-msg-file

# This module converts a Microsoft Outlook .msg file into
# a MIME message that can be loaded by most email programs
# or inspected in a text editor.
#
# This script relies on the Python package compoundfiles
# for reading the .msg container format.
#
# References:
#
# https://msdn.microsoft.com/en-us/library/cc463912.aspx
# https://msdn.microsoft.com/en-us/library/cc463900(v=exchg.80).aspx
# https://msdn.microsoft.com/en-us/library/ee157583(v=exchg.80).aspx
# https://blogs.msdn.microsoft.com/openspecification/2009/11/06/msg-file-format-part-1/

import email.message
import email.parser
import email.policy
import os
import re
from email.message import EmailMessage
from email.utils import formataddr, formatdate
from functools import reduce
from typing import BinaryIO

import compressed_rtf
from compoundfiles import CompoundFileEntity, CompoundFileReader
from loguru import logger

FALLBACK_ENCODING = "cp1252"


class Message:
    def __init__(self, filename_or_stream: str | BinaryIO):
        self.filename_or_stream = filename_or_stream

    def to_email(self) -> EmailMessage:
        with CompoundFileReader(self.filename_or_stream) as doc:
            doc.rtf_attachments = 0
            return load_message_stream(doc.root, True, doc)


def load_message_stream(  # noqa: C901
    entry: CompoundFileEntity, is_top_level: bool, doc: CompoundFileReader
):
    # Load stream data.
    props = parse_properties(entry["__properties_version1.0"], is_top_level, entry, doc)

    # Construct the MIME message....
    msg = email.message.EmailMessage()

    # Add the raw headers, if known.
    if "TRANSPORT_MESSAGE_HEADERS" in props:
        # Get the string holding all of the headers.
        headers = props["TRANSPORT_MESSAGE_HEADERS"]
        if isinstance(headers, bytes):
            headers = headers.decode("utf-8")

        # Remove content-type header because the body we can get this
        # way is just the plain-text portion of the email and whatever
        # Content-Type header was in the original is not valid for
        # reconstructing it this way.
        headers = re.sub("Content-Type: .*(\n\\s.*)*\n", "", headers, re.I)  # noqa: B034

        # Parse them.
        headers = email.parser.HeaderParser(policy=email.policy.default).parsestr(
            headers
        )

        # Copy them into the message object.
        for header, value in headers.items():
            msg[header] = value

    else:
        # Construct common headers from metadata.

        if "MESSAGE_DELIVERY_TIME" in props:
            msg["Date"] = formatdate(props["MESSAGE_DELIVERY_TIME"].timestamp())
            del props["MESSAGE_DELIVERY_TIME"]

        if "SENDER_NAME" in props:
            if "SENT_REPRESENTING_NAME" in props:
                if props["SENT_REPRESENTING_NAME"]:  # noqa: SIM102
                    if props["SENDER_NAME"] != props["SENT_REPRESENTING_NAME"]:
                        props["SENDER_NAME"] += (
                            " (" + props["SENT_REPRESENTING_NAME"] + ")"
                        )
                del props["SENT_REPRESENTING_NAME"]
            if props["SENDER_NAME"]:
                msg["From"] = formataddr((props["SENDER_NAME"], ""))
            del props["SENDER_NAME"]

        if "DISPLAY_TO" in props:
            if props["DISPLAY_TO"]:
                msg["To"] = props["DISPLAY_TO"]
            del props["DISPLAY_TO"]

        if "DISPLAY_CC" in props:
            if props["DISPLAY_CC"]:
                msg["CC"] = props["DISPLAY_CC"]
            del props["DISPLAY_CC"]

        if "DISPLAY_BCC" in props:
            if props["DISPLAY_BCC"]:
                msg["BCC"] = props["DISPLAY_BCC"]
            del props["DISPLAY_BCC"]

        if "SUBJECT" in props:
            if props["SUBJECT"]:
                msg["Subject"] = props["SUBJECT"]
            del props["SUBJECT"]

    # Add the plain-text body from the BODY field.
    if "BODY" in props:
        body = props["BODY"]
        if isinstance(body, str):
            msg.set_content(body, cte="quoted-printable")
        else:
            msg.set_content(body, maintype="text", subtype="plain", cte="8bit")

    # Plain-text is not availabe. Use the rich text version.
    else:
        doc.rtf_attachments += 1
        fn = f"messagebody_{doc.rtf_attachments}.rtf"

        msg.set_content(
            f"<no plain text message body --- see attachment {fn}>",
            cte="quoted-printable",
        )

        # Decompress the value to Rich Text Format.
        rtf = props["RTF_COMPRESSED"]
        rtf = compressed_rtf.decompress(rtf)

        # Add RTF file as an attachment.
        msg.add_attachment(rtf, maintype="text", subtype="rtf", filename=fn)

    # # Copy over string values of remaining properties as headers
    # # so we don't lose any information.
    # for k, v in props.items():
    #   if k == 'RTF_COMPRESSED': continue # not interested, save output
    #   msg[k] = str(v)

    # Add attachments.
    for stream in entry:
        if stream.name.startswith("__attach_version1.0_#"):
            process_attachment(msg, stream, doc)

    return msg


def process_attachment(
    msg: EmailMessage, entry: CompoundFileEntity, doc: CompoundFileReader
):
    # Load attachment stream.
    props = parse_properties(entry["__properties_version1.0"], False, entry, doc)

    # The attachment content...
    blob = props["ATTACH_DATA_BIN"]

    # Get the filename and MIME type of the attachment.
    filename = (
        props.get("ATTACH_LONG_FILENAME")
        or props.get("ATTACH_FILENAME")
        or props.get("DISPLAY_NAME")
    )
    if isinstance(filename, bytes):
        filename = filename.decode("utf8")

    mime_type = props.get("ATTACH_MIME_TAG", "application/octet-stream")
    if isinstance(mime_type, bytes):
        mime_type = mime_type.decode("utf8")

    filename = os.path.basename(filename)

    # Python 3.6.
    if isinstance(blob, str):
        msg.add_attachment(blob, filename=filename)
    elif isinstance(blob, bytes):
        msg.add_attachment(
            blob,
            maintype=mime_type.split("/", 1)[0],
            subtype=mime_type.split("/", 1)[-1],
            filename=filename,
        )
    else:  # a Message instance
        msg.add_attachment(blob, filename=filename)


def parse_properties(  # noqa: C901
    properties: CompoundFileEntity,
    is_top_level: bool,
    container: CompoundFileEntity,
    doc: CompoundFileReader,
):
    # Read a properties stream and return a Python dictionary
    # of the fields and values, using human-readable field names
    # in the mapping at the top of this module.

    # Load stream content.
    with doc.open(properties) as stream:
        stream = stream.read()

    # Skip header.
    i = 32 if is_top_level else 24

    # Read 16-byte entries.
    raw_properties = {}
    while i < len(stream):
        # Read the entry.
        property_type = stream[i + 0 : i + 2]
        property_tag = stream[i + 2 : i + 4]
        # flags = stream[i+4:i+8]
        value = stream[i + 8 : i + 16]
        i += 16

        # Turn the byte strings into numbers and look up the property type.
        property_type = property_type[0] + (property_type[1] << 8)
        property_tag = property_tag[0] + (property_tag[1] << 8)
        if property_tag not in property_tags:
            continue  # should not happen
        tag_name, _ = property_tags[property_tag]
        tag_type = property_types.get(property_type)

        # Fixed Length Properties.
        if isinstance(tag_type, FixedLengthValueLoader):
            # The value comes from the stream above.
            pass

        # Variable Length Properties.
        elif isinstance(tag_type, VariableLengthValueLoader):
            # value_length = stream[i + 8 : i + 12]  # not used

            # Look up the stream in the document that holds the value.
            streamname = "__substg1.0_{0:0{1}X}{2:0{3}X}".format(
                property_tag, 4, property_type, 4
            )
            try:
                with doc.open(container[streamname]) as innerstream:
                    value = innerstream.read()
            except Exception:
                # Stream isn't present!
                logger.error("stream missing {}".format(streamname))
                continue

        elif isinstance(tag_type, EMBEDDED_MESSAGE):
            # Look up the stream in the document that holds the attachment.
            streamname = "__substg1.0_{0:0{1}X}{2:0{3}X}".format(
                property_tag, 4, property_type, 4
            )
            try:
                value = container[streamname]
            except Exception:
                # Stream isn't present!
                logger.error("stream missing {}".format(streamname))
                continue

        else:
            # unrecognized type
            logger.error("unhandled property type {}".format(hex(property_type)))
            continue

        raw_properties[tag_name] = (tag_type, value)

    # Decode all FixedLengthValueLoader properties so we have codepage
    # properties.
    properties = {}
    for tag_name, (tag_type, value) in raw_properties.items():
        if not isinstance(tag_type, FixedLengthValueLoader):
            continue
        try:
            properties[tag_name] = tag_type.load(value)
        except Exception as e:
            logger.error("Error while reading stream: {}".format(str(e)))

    # String8 strings use code page information stored in other
    # properties, which may not be present. Find the Python
    # encoding to use.

    # The encoding of the "BODY" (and HTML body) properties.
    body_encoding = None
    if (
        "PR_INTERNET_CPID" in properties
        and properties["PR_INTERNET_CPID"] in code_pages
    ):
        body_encoding = code_pages[properties["PR_INTERNET_CPID"]]

    # The encoding of "string properties of the message object".
    properties_encoding = None
    if (
        "PR_MESSAGE_CODEPAGE" in properties
        and properties["PR_MESSAGE_CODEPAGE"] in code_pages
    ):
        properties_encoding = code_pages[properties["PR_MESSAGE_CODEPAGE"]]

    # Decode all of the remaining properties.
    for tag_name, (tag_type, value) in raw_properties.items():
        if isinstance(tag_type, FixedLengthValueLoader):
            continue  # already done, above

        # The codepage properties may be wrong. Fall back to
        # the other property if present.
        encodings = (
            [body_encoding, properties_encoding]
            if tag_name == "BODY"
            else [properties_encoding, body_encoding]
        )

        try:
            properties[tag_name] = tag_type.load(value, encodings=encodings, doc=doc)
        except KeyError as e:
            logger.error("Error while reading stream: {} not found".format(str(e)))
        except Exception as e:
            logger.error("Error while reading stream: {}".format(str(e)))

    return properties


class FixedLengthValueLoader:
    @staticmethod
    def load(value):
        raise NotImplementedError()


class NULL(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring with unused content.
        return None


class BOOLEAN(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring holding a two-byte integer.
        return value[0] == 1


class INTEGER16(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring holding a two-byte integer.
        return reduce(lambda a, b: (a << 8) + b, reversed(value[0:2]))


class INTEGER32(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring holding a four-byte integer.
        return reduce(lambda a, b: (a << 8) + b, reversed(value[0:4]))


class INTEGER64(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring holding an eight-byte integer.
        return reduce(lambda a, b: (a << 8) + b, reversed(value))


class INTTIME(FixedLengthValueLoader):
    @staticmethod
    def load(value):
        # value is an eight-byte long bytestring encoding the integer number of
        # 100-nanosecond intervals since January 1, 1601.
        from datetime import datetime, timedelta

        value = reduce(
            lambda a, b: (a << 8) + b, reversed(value)
        )  # bytestring to integer
        return datetime(1601, 1, 1) + timedelta(seconds=value / 10000000)


# TODO: The other fixed-length data types:
# "FLOAT", "DOUBLE", "CURRENCY", "APPTIME", "ERROR"


class VariableLengthValueLoader:
    @staticmethod
    def load(value):
        raise NotImplementedError()


class BINARY(VariableLengthValueLoader):
    @staticmethod
    def load(value, **kwargs):
        # value is a bytestring. Just return it.
        return value


class STRING8(VariableLengthValueLoader):
    @staticmethod
    def load(value, encodings, **kwargs):
        # Value is a "bytestring" and encodings is a list of Python
        # codecs to try. If all fail, try the fallback codec with
        # character replacement so that this never fails.
        for encoding in encodings:
            try:
                return value.decode(encoding=encoding, errors="strict")
            except Exception:
                # Try the next one.
                pass
        return value.decode(encoding=FALLBACK_ENCODING, errors="replace")


class UNICODE(VariableLengthValueLoader):
    @staticmethod
    def load(value, **kwargs):
        # value is a bytestring encoded in UTF-16.
        return value.decode("utf16")


# TODO: The other variable-length tag types are "CLSID", "OBJECT".


class EMBEDDED_MESSAGE:  # noqa: N801
    @staticmethod
    def load(entry, doc, **kwargs):
        return load_message_stream(entry, False, doc)


# CONSTANTS

# These constants are defined by the Microsoft Outlook file format
# and identify the data types and data fields in the .msg file.

# from mapidefs.h via https://github.com/inverse-inc/openchange.old/blob/master/libmapi/mapidefs.h
property_types = {
    0x1: NULL(),
    0x2: INTEGER16(),
    0x3: INTEGER32(),
    0x4: "FLOAT",
    0x5: "DOUBLE",
    0x6: "CURRENCY",
    0x7: "APPTIME",
    0xA: "ERROR",
    0xB: BOOLEAN(),
    0xD: EMBEDDED_MESSAGE(),
    0x14: INTEGER64(),
    0x1E: STRING8(),
    0x1F: UNICODE(),
    0x40: INTTIME(),
    0x48: "CLSID",
    0xFB: "SVREID",
    0xFD: "SRESTRICT",
    0xFE: "ACTIONS",
    0x102: BINARY(),
}

# from mapitags.h via https://github.com/mvz/email-outlook-message-perl/blob/master/mapitags.h
property_tags = {
    0x01: ("ACKNOWLEDGEMENT_MODE", "I4"),
    0x02: ("ALTERNATE_RECIPIENT_ALLOWED", "BOOLEAN"),
    0x03: ("AUTHORIZING_USERS", "BINARY"),
    # Comment on an automatically forwarded message
    0x04: ("AUTO_FORWARD_COMMENT", "STRING"),
    # Whether a message has been automatically forwarded
    0x05: ("AUTO_FORWARDED", "BOOLEAN"),
    0x06: ("CONTENT_CONFIDENTIALITY_ALGORITHM_ID", "BINARY"),
    0x07: ("CONTENT_CORRELATOR", "BINARY"),
    0x08: ("CONTENT_IDENTIFIER", "STRING"),
    # MIME content length
    0x09: ("CONTENT_LENGTH", "I4"),
    0x0A: ("CONTENT_RETURN_REQUESTED", "BOOLEAN"),
    0x0B: ("CONVERSATION_KEY", "BINARY"),
    0x0C: ("CONVERSION_EITS", "BINARY"),
    0x0D: ("CONVERSION_WITH_LOSS_PROHIBITED", "BOOLEAN"),
    0x0E: ("CONVERTED_EITS", "BINARY"),
    # Time to deliver for delayed delivery messages
    0x0F: ("DEFERRED_DELIVERY_TIME", "SYSTIME"),
    0x10: ("DELIVER_TIME", "SYSTIME"),
    # Reason a message was discarded
    0x11: ("DISCARD_REASON", "I4"),
    0x12: ("DISCLOSURE_OF_RECIPIENTS", "BOOLEAN"),
    0x13: ("DL_EXPANSION_HISTORY", "BINARY"),
    0x14: ("DL_EXPANSION_PROHIBITED", "BOOLEAN"),
    0x15: ("EXPIRY_TIME", "SYSTIME"),
    0x16: ("IMPLICIT_CONVERSION_PROHIBITED", "BOOLEAN"),
    # Message importance
    0x17: ("IMPORTANCE", "I4"),
    0x18: ("IPM_ID", "BINARY"),
    0x19: ("LATEST_DELIVERY_TIME", "SYSTIME"),
    0x1A: ("MESSAGE_CLASS", "STRING"),
    0x1B: ("MESSAGE_DELIVERY_ID", "BINARY"),
    0x1E: ("MESSAGE_SECURITY_LABEL", "BINARY"),
    0x1F: ("OBSOLETED_IPMS", "BINARY"),
    # Person a message was originally for
    0x20: ("ORIGINALLY_INTENDED_RECIPIENT_NAME", "BINARY"),
    0x21: ("ORIGINAL_EITS", "BINARY"),
    0x22: ("ORIGINATOR_CERTIFICATE", "BINARY"),
    0x23: ("ORIGINATOR_DELIVERY_REPORT_REQUESTED", "BOOLEAN"),
    # Address of the message sender
    0x24: ("ORIGINATOR_RETURN_ADDRESS", "BINARY"),
    0x25: ("PARENT_KEY", "BINARY"),
    0x26: ("PRIORITY", "I4"),
    0x27: ("ORIGIN_CHECK", "BINARY"),
    0x28: ("PROOF_OF_SUBMISSION_REQUESTED", "BOOLEAN"),
    # Whether a read receipt is desired
    0x29: ("READ_RECEIPT_REQUESTED", "BOOLEAN"),
    # Time a message was received
    0x2A: ("RECEIPT_TIME", "SYSTIME"),
    0x2B: ("RECIPIENT_REASSIGNMENT_PROHIBITED", "BOOLEAN"),
    0x2C: ("REDIRECTION_HISTORY", "BINARY"),
    0x2D: ("RELATED_IPMS", "BINARY"),
    # Sensitivity of the original message
    0x2E: ("ORIGINAL_SENSITIVITY", "I4"),
    0x2F: ("LANGUAGES", "STRING"),
    0x30: ("REPLY_TIME", "SYSTIME"),
    0x31: ("REPORT_TAG", "BINARY"),
    0x32: ("REPORT_TIME", "SYSTIME"),
    0x33: ("RETURNED_IPM", "BOOLEAN"),
    0x34: ("SECURITY", "I4"),
    0x35: ("INCOMPLETE_COPY", "BOOLEAN"),
    0x36: ("SENSITIVITY", "I4"),
    # The message subject
    0x37: ("SUBJECT", "STRING"),
    0x38: ("SUBJECT_IPM", "BINARY"),
    0x39: ("CLIENT_SUBMIT_TIME", "SYSTIME"),
    0x3A: ("REPORT_NAME", "STRING"),
    0x3B: ("SENT_REPRESENTING_SEARCH_KEY", "BINARY"),
    0x3C: ("X400_CONTENT_TYPE", "BINARY"),
    0x3D: ("SUBJECT_PREFIX", "STRING"),
    0x3E: ("NON_RECEIPT_REASON", "I4"),
    0x3F: ("RECEIVED_BY_ENTRYID", "BINARY"),
    # Received by: entry
    0x40: ("RECEIVED_BY_NAME", "STRING"),
    0x41: ("SENT_REPRESENTING_ENTRYID", "BINARY"),
    0x42: ("SENT_REPRESENTING_NAME", "STRING"),
    0x43: ("RCVD_REPRESENTING_ENTRYID", "BINARY"),
    0x44: ("RCVD_REPRESENTING_NAME", "STRING"),
    0x45: ("REPORT_ENTRYID", "BINARY"),
    0x46: ("READ_RECEIPT_ENTRYID", "BINARY"),
    0x47: ("MESSAGE_SUBMISSION_ID", "BINARY"),
    0x48: ("PROVIDER_SUBMIT_TIME", "SYSTIME"),
    # Subject of the original message
    0x49: ("ORIGINAL_SUBJECT", "STRING"),
    0x4A: ("DISC_VAL", "BOOLEAN"),
    0x4B: ("ORIG_MESSAGE_CLASS", "STRING"),
    0x4C: ("ORIGINAL_AUTHOR_ENTRYID", "BINARY"),
    # Author of the original message
    0x4D: ("ORIGINAL_AUTHOR_NAME", "STRING"),
    # Time the original message was submitted
    0x4E: ("ORIGINAL_SUBMIT_TIME", "SYSTIME"),
    0x4F: ("REPLY_RECIPIENT_ENTRIES", "BINARY"),
    0x50: ("REPLY_RECIPIENT_NAMES", "STRING"),
    0x51: ("RECEIVED_BY_SEARCH_KEY", "BINARY"),
    0x52: ("RCVD_REPRESENTING_SEARCH_KEY", "BINARY"),
    0x53: ("READ_RECEIPT_SEARCH_KEY", "BINARY"),
    0x54: ("REPORT_SEARCH_KEY", "BINARY"),
    0x55: ("ORIGINAL_DELIVERY_TIME", "SYSTIME"),
    0x56: ("ORIGINAL_AUTHOR_SEARCH_KEY", "BINARY"),
    0x57: ("MESSAGE_TO_ME", "BOOLEAN"),
    0x58: ("MESSAGE_CC_ME", "BOOLEAN"),
    0x59: ("MESSAGE_RECIP_ME", "BOOLEAN"),
    # Sender of the original message
    0x5A: ("ORIGINAL_SENDER_NAME", "STRING"),
    0x5B: ("ORIGINAL_SENDER_ENTRYID", "BINARY"),
    0x5C: ("ORIGINAL_SENDER_SEARCH_KEY", "BINARY"),
    0x5D: ("ORIGINAL_SENT_REPRESENTING_NAME", "STRING"),
    0x5E: ("ORIGINAL_SENT_REPRESENTING_ENTRYID", "BINARY"),
    0x5F: ("ORIGINAL_SENT_REPRESENTING_SEARCH_KEY", "BINARY"),
    0x60: ("START_DATE", "SYSTIME"),
    0x61: ("END_DATE", "SYSTIME"),
    0x62: ("OWNER_APPT_ID", "I4"),
    # Whether a response to the message is desired
    0x63: ("RESPONSE_REQUESTED", "BOOLEAN"),
    0x64: ("SENT_REPRESENTING_ADDRTYPE", "STRING"),
    0x65: ("SENT_REPRESENTING_EMAIL_ADDRESS", "STRING"),
    0x66: ("ORIGINAL_SENDER_ADDRTYPE", "STRING"),
    # Email of the original message sender
    0x67: ("ORIGINAL_SENDER_EMAIL_ADDRESS", "STRING"),
    0x68: ("ORIGINAL_SENT_REPRESENTING_ADDRTYPE", "STRING"),
    0x69: ("ORIGINAL_SENT_REPRESENTING_EMAIL_ADDRESS", "STRING"),
    0x70: ("CONVERSATION_TOPIC", "STRING"),
    0x71: ("CONVERSATION_INDEX", "BINARY"),
    0x72: ("ORIGINAL_DISPLAY_BCC", "STRING"),
    0x73: ("ORIGINAL_DISPLAY_CC", "STRING"),
    0x74: ("ORIGINAL_DISPLAY_TO", "STRING"),
    0x75: ("RECEIVED_BY_ADDRTYPE", "STRING"),
    0x76: ("RECEIVED_BY_EMAIL_ADDRESS", "STRING"),
    0x77: ("RCVD_REPRESENTING_ADDRTYPE", "STRING"),
    0x78: ("RCVD_REPRESENTING_EMAIL_ADDRESS", "STRING"),
    0x79: ("ORIGINAL_AUTHOR_ADDRTYPE", "STRING"),
    0x7A: ("ORIGINAL_AUTHOR_EMAIL_ADDRESS", "STRING"),
    0x7B: ("ORIGINALLY_INTENDED_RECIP_ADDRTYPE", "STRING"),
    0x7C: ("ORIGINALLY_INTENDED_RECIP_EMAIL_ADDRESS", "STRING"),
    0x7D: ("TRANSPORT_MESSAGE_HEADERS", "STRING"),
    0x7E: ("DELEGATION", "BINARY"),
    0x7F: ("TNEF_CORRELATION_KEY", "BINARY"),
    0x1000: ("BODY", "STRING"),
    0x1001: ("REPORT_TEXT", "STRING"),
    0x1002: ("ORIGINATOR_AND_DL_EXPANSION_HISTORY", "BINARY"),
    0x1003: ("REPORTING_DL_NAME", "BINARY"),
    0x1004: ("REPORTING_MTA_CERTIFICATE", "BINARY"),
    0x1006: ("RTF_SYNC_BODY_CRC", "I4"),
    0x1007: ("RTF_SYNC_BODY_COUNT", "I4"),
    0x1008: ("RTF_SYNC_BODY_TAG", "STRING"),
    0x1009: ("RTF_COMPRESSED", "BINARY"),
    0x1010: ("RTF_SYNC_PREFIX_COUNT", "I4"),
    0x1011: ("RTF_SYNC_TRAILING_COUNT", "I4"),
    0x1012: ("ORIGINALLY_INTENDED_RECIP_ENTRYID", "BINARY"),
    0x0C00: ("CONTENT_INTEGRITY_CHECK", "BINARY"),
    0x0C01: ("EXPLICIT_CONVERSION", "I4"),
    0x0C02: ("IPM_RETURN_REQUESTED", "BOOLEAN"),
    0x0C03: ("MESSAGE_TOKEN", "BINARY"),
    0x0C04: ("NDR_REASON_CODE", "I4"),
    0x0C05: ("NDR_DIAG_CODE", "I4"),
    0x0C06: ("NON_RECEIPT_NOTIFICATION_REQUESTED", "BOOLEAN"),
    0x0C07: ("DELIVERY_POINT", "I4"),
    0x0C08: ("ORIGINATOR_NON_DELIVERY_REPORT_REQUESTED", "BOOLEAN"),
    0x0C09: ("ORIGINATOR_REQUESTED_ALTERNATE_RECIPIENT", "BINARY"),
    0x0C0A: ("PHYSICAL_DELIVERY_BUREAU_FAX_DELIVERY", "BOOLEAN"),
    0x0C0B: ("PHYSICAL_DELIVERY_MODE", "I4"),
    0x0C0C: ("PHYSICAL_DELIVERY_REPORT_REQUEST", "I4"),
    0x0C0D: ("PHYSICAL_FORWARDING_ADDRESS", "BINARY"),
    0x0C0E: ("PHYSICAL_FORWARDING_ADDRESS_REQUESTED", "BOOLEAN"),
    0x0C0F: ("PHYSICAL_FORWARDING_PROHIBITED", "BOOLEAN"),
    0x0C10: ("PHYSICAL_RENDITION_ATTRIBUTES", "BINARY"),
    0x0C11: ("PROOF_OF_DELIVERY", "BINARY"),
    0x0C12: ("PROOF_OF_DELIVERY_REQUESTED", "BOOLEAN"),
    0x0C13: ("RECIPIENT_CERTIFICATE", "BINARY"),
    0x0C14: ("RECIPIENT_NUMBER_FOR_ADVICE", "STRING"),
    0x0C15: ("RECIPIENT_TYPE", "I4"),
    0x0C16: ("REGISTERED_MAIL_TYPE", "I4"),
    0x0C17: ("REPLY_REQUESTED", "BOOLEAN"),
    0x0C18: ("REQUESTED_DELIVERY_METHOD", "I4"),
    0x0C19: ("SENDER_ENTRYID", "BINARY"),
    0x0C1A: ("SENDER_NAME", "STRING"),
    0x0C1B: ("SUPPLEMENTARY_INFO", "STRING"),
    0x0C1C: ("TYPE_OF_MTS_USER", "I4"),
    0x0C1D: ("SENDER_SEARCH_KEY", "BINARY"),
    0x0C1E: ("SENDER_ADDRTYPE", "STRING"),
    0x0C1F: ("SENDER_EMAIL_ADDRESS", "STRING"),
    0x0E00: ("CURRENT_VERSION", "I8"),
    0x0E01: ("DELETE_AFTER_SUBMIT", "BOOLEAN"),
    0x0E02: ("DISPLAY_BCC", "STRING"),
    0x0E03: ("DISPLAY_CC", "STRING"),
    0x0E04: ("DISPLAY_TO", "STRING"),
    0x0E05: ("PARENT_DISPLAY", "STRING"),
    0x0E06: ("MESSAGE_DELIVERY_TIME", "SYSTIME"),
    0x0E07: ("MESSAGE_FLAGS", "I4"),
    0x0E08: ("MESSAGE_SIZE", "I4"),
    0x0E09: ("PARENT_ENTRYID", "BINARY"),
    0x0E0A: ("SENTMAIL_ENTRYID", "BINARY"),
    0x0E0C: ("CORRELATE", "BOOLEAN"),
    0x0E0D: ("CORRELATE_MTSID", "BINARY"),
    0x0E0E: ("DISCRETE_VALUES", "BOOLEAN"),
    0x0E0F: ("RESPONSIBILITY", "BOOLEAN"),
    0x0E10: ("SPOOLER_STATUS", "I4"),
    0x0E11: ("TRANSPORT_STATUS", "I4"),
    0x0E12: ("MESSAGE_RECIPIENTS", "OBJECT"),
    0x0E13: ("MESSAGE_ATTACHMENTS", "OBJECT"),
    0x0E14: ("SUBMIT_FLAGS", "I4"),
    0x0E15: ("RECIPIENT_STATUS", "I4"),
    0x0E16: ("TRANSPORT_KEY", "I4"),
    0x0E17: ("MSG_STATUS", "I4"),
    0x0E18: ("MESSAGE_DOWNLOAD_TIME", "I4"),
    0x0E19: ("CREATION_VERSION", "I8"),
    0x0E1A: ("MODIFY_VERSION", "I8"),
    0x0E1B: ("HASATTACH", "BOOLEAN"),
    0x0E1D: ("NORMALIZED_SUBJECT", "STRING"),
    0x0E1F: ("RTF_IN_SYNC", "BOOLEAN"),
    0x0E20: ("ATTACH_SIZE", "I4"),
    0x0E21: ("ATTACH_NUM", "I4"),
    0x0E22: ("PREPROCESS", "BOOLEAN"),
    0x0E25: ("ORIGINATING_MTA_CERTIFICATE", "BINARY"),
    0x0E26: ("PROOF_OF_SUBMISSION", "BINARY"),
    # A unique identifier for editing the properties of a MAPI object
    0x0FFF: ("ENTRYID", "BINARY"),
    # The type of an object
    0x0FFE: ("OBJECT_TYPE", "I4"),
    0x0FFD: ("ICON", "BINARY"),
    0x0FFC: ("MINI_ICON", "BINARY"),
    0x0FFB: ("STORE_ENTRYID", "BINARY"),
    0x0FFA: ("STORE_RECORD_KEY", "BINARY"),
    # Binary identifer for an individual object
    0x0FF9: ("RECORD_KEY", "BINARY"),
    0x0FF8: ("MAPPING_SIGNATURE", "BINARY"),
    0x0FF7: ("ACCESS_LEVEL", "I4"),
    # The primary key of a column in a table
    0x0FF6: ("INSTANCE_KEY", "BINARY"),
    0x0FF5: ("ROW_TYPE", "I4"),
    0x0FF4: ("ACCESS", "I4"),
    0x3000: ("ROWID", "I4"),
    # The name to display for a given MAPI object
    0x3001: ("DISPLAY_NAME", "STRING"),
    0x3002: ("ADDRTYPE", "STRING"),
    # An email address
    0x3003: ("EMAIL_ADDRESS", "STRING"),
    # A comment field
    0x3004: ("COMMENT", "STRING"),
    0x3005: ("DEPTH", "I4"),
    # Provider-defined display name for a service provider
    0x3006: ("PROVIDER_DISPLAY", "STRING"),
    # The time an object was created
    0x3007: ("CREATION_TIME", "SYSTIME"),
    # The time an object was last modified
    0x3008: ("LAST_MODIFICATION_TIME", "SYSTIME"),
    # Flags describing a service provider, message service, or status object
    0x3009: ("RESOURCE_FLAGS", "I4"),
    # The name of a provider dll, minus any "32" suffix and ".dll"
    0x300A: ("PROVIDER_DLL_NAME", "STRING"),
    0x300B: ("SEARCH_KEY", "BINARY"),
    0x300C: ("PROVIDER_UID", "BINARY"),
    0x300D: ("PROVIDER_ORDINAL", "I4"),
    0x3301: ("FORM_VERSION", "STRING"),
    0x3302: ("FORM_CLSID", "CLSID"),
    0x3303: ("FORM_CONTACT_NAME", "STRING"),
    0x3304: ("FORM_CATEGORY", "STRING"),
    0x3305: ("FORM_CATEGORY_SUB", "STRING"),
    0x3306: ("FORM_HOST_MAP", "MV_LONG"),
    0x3307: ("FORM_HIDDEN", "BOOLEAN"),
    0x3308: ("FORM_DESIGNER_NAME", "STRING"),
    0x3309: ("FORM_DESIGNER_GUID", "CLSID"),
    0x330A: ("FORM_MESSAGE_BEHAVIOR", "I4"),
    # Is this row the default message store?
    0x3400: ("DEFAULT_STORE", "BOOLEAN"),
    0x340D: ("STORE_SUPPORT_MASK", "I4"),
    0x340E: ("STORE_STATE", "I4"),
    0x3410: ("IPM_SUBTREE_SEARCH_KEY", "BINARY"),
    0x3411: ("IPM_OUTBOX_SEARCH_KEY", "BINARY"),
    0x3412: ("IPM_WASTEBASKET_SEARCH_KEY", "BINARY"),
    0x3413: ("IPM_SENTMAIL_SEARCH_KEY", "BINARY"),
    # Provder-defined message store type
    0x3414: ("MDB_PROVIDER", "BINARY"),
    0x3415: ("RECEIVE_FOLDER_SETTINGS", "OBJECT"),
    0x35DF: ("VALID_FOLDER_MASK", "I4"),
    0x35E0: ("IPM_SUBTREE_ENTRYID", "BINARY"),
    0x35E2: ("IPM_OUTBOX_ENTRYID", "BINARY"),
    0x35E3: ("IPM_WASTEBASKET_ENTRYID", "BINARY"),
    0x35E4: ("IPM_SENTMAIL_ENTRYID", "BINARY"),
    0x35E5: ("VIEWS_ENTRYID", "BINARY"),
    0x35E6: ("COMMON_VIEWS_ENTRYID", "BINARY"),
    0x35E7: ("FINDER_ENTRYID", "BINARY"),
    0x3600: ("CONTAINER_FLAGS", "I4"),
    0x3601: ("FOLDER_TYPE", "I4"),
    0x3602: ("CONTENT_COUNT", "I4"),
    0x3603: ("CONTENT_UNREAD", "I4"),
    0x3604: ("CREATE_TEMPLATES", "OBJECT"),
    0x3605: ("DETAILS_TABLE", "OBJECT"),
    0x3607: ("SEARCH", "OBJECT"),
    0x3609: ("SELECTABLE", "BOOLEAN"),
    0x360A: ("SUBFOLDERS", "BOOLEAN"),
    0x360B: ("STATUS", "I4"),
    0x360C: ("ANR", "STRING"),
    0x360D: ("CONTENTS_SORT_ORDER", "MV_LONG"),
    0x360E: ("CONTAINER_HIERARCHY", "OBJECT"),
    0x360F: ("CONTAINER_CONTENTS", "OBJECT"),
    0x3610: ("FOLDER_ASSOCIATED_CONTENTS", "OBJECT"),
    0x3611: ("DEF_CREATE_DL", "BINARY"),
    0x3612: ("DEF_CREATE_MAILUSER", "BINARY"),
    0x3613: ("CONTAINER_CLASS", "STRING"),
    0x3614: ("CONTAINER_MODIFY_VERSION", "I8"),
    0x3615: ("AB_PROVIDER_ID", "BINARY"),
    0x3616: ("DEFAULT_VIEW_ENTRYID", "BINARY"),
    0x3617: ("ASSOC_CONTENT_COUNT", "I4"),
    0x3700: ("ATTACHMENT_X400_PARAMETERS", "BINARY"),
    # 0x3701: ("ATTACH_DATA_OBJ", "OBJECT"),
    0x3701: ("ATTACH_DATA_BIN", "BINARY"),
    0x3702: ("ATTACH_ENCODING", "BINARY"),
    0x3703: ("ATTACH_EXTENSION", "STRING"),
    0x3704: ("ATTACH_FILENAME", "STRING"),
    0x3705: ("ATTACH_METHOD", "I4"),
    0x3707: ("ATTACH_LONG_FILENAME", "STRING"),
    0x3708: ("ATTACH_PATHNAME", "STRING"),
    0x370A: ("ATTACH_TAG", "BINARY"),
    0x370B: ("RENDERING_POSITION", "I4"),
    0x370C: ("ATTACH_TRANSPORT_NAME", "STRING"),
    0x370D: ("ATTACH_LONG_PATHNAME", "STRING"),
    0x370E: ("ATTACH_MIME_TAG", "STRING"),
    0x370F: ("ATTACH_ADDITIONAL_INFO", "BINARY"),
    0x3900: ("DISPLAY_TYPE", "I4"),
    0x3902: ("TEMPLATEID", "BINARY"),
    0x3904: ("PRIMARY_CAPABILITY", "BINARY"),
    0x39FF: ("7BIT_DISPLAY_NAME", "STRING"),
    0x3A00: ("ACCOUNT", "STRING"),
    0x3A01: ("ALTERNATE_RECIPIENT", "BINARY"),
    0x3A02: ("CALLBACK_TELEPHONE_NUMBER", "STRING"),
    0x3A03: ("CONVERSION_PROHIBITED", "BOOLEAN"),
    0x3A04: ("DISCLOSE_RECIPIENTS", "BOOLEAN"),
    0x3A05: ("GENERATION", "STRING"),
    0x3A06: ("GIVEN_NAME", "STRING"),
    0x3A07: ("GOVERNMENT_ID_NUMBER", "STRING"),
    0x3A08: ("BUSINESS_TELEPHONE_NUMBER", "STRING"),
    0x3A09: ("HOME_TELEPHONE_NUMBER", "STRING"),
    0x3A0A: ("INITIALS", "STRING"),
    0x3A0B: ("KEYWORD", "STRING"),
    0x3A0C: ("LANGUAGE", "STRING"),
    0x3A0D: ("LOCATION", "STRING"),
    0x3A0E: ("MAIL_PERMISSION", "BOOLEAN"),
    0x3A0F: ("MHS_COMMON_NAME", "STRING"),
    0x3A10: ("ORGANIZATIONAL_ID_NUMBER", "STRING"),
    0x3A11: ("SURNAME", "STRING"),
    0x3A12: ("ORIGINAL_ENTRYID", "BINARY"),
    0x3A13: ("ORIGINAL_DISPLAY_NAME", "STRING"),
    0x3A14: ("ORIGINAL_SEARCH_KEY", "BINARY"),
    0x3A15: ("POSTAL_ADDRESS", "STRING"),
    0x3A16: ("COMPANY_NAME", "STRING"),
    0x3A17: ("TITLE", "STRING"),
    0x3A18: ("DEPARTMENT_NAME", "STRING"),
    0x3A19: ("OFFICE_LOCATION", "STRING"),
    0x3A1A: ("PRIMARY_TELEPHONE_NUMBER", "STRING"),
    0x3A1B: ("BUSINESS2_TELEPHONE_NUMBER", "STRING"),
    0x3A1C: ("MOBILE_TELEPHONE_NUMBER", "STRING"),
    0x3A1D: ("RADIO_TELEPHONE_NUMBER", "STRING"),
    0x3A1E: ("CAR_TELEPHONE_NUMBER", "STRING"),
    0x3A1F: ("OTHER_TELEPHONE_NUMBER", "STRING"),
    0x3A20: ("TRANSMITABLE_DISPLAY_NAME", "STRING"),
    0x3A21: ("PAGER_TELEPHONE_NUMBER", "STRING"),
    0x3A22: ("USER_CERTIFICATE", "BINARY"),
    0x3A23: ("PRIMARY_FAX_NUMBER", "STRING"),
    0x3A24: ("BUSINESS_FAX_NUMBER", "STRING"),
    0x3A25: ("HOME_FAX_NUMBER", "STRING"),
    0x3A26: ("COUNTRY", "STRING"),
    0x3A27: ("LOCALITY", "STRING"),
    0x3A28: ("STATE_OR_PROVINCE", "STRING"),
    0x3A29: ("STREET_ADDRESS", "STRING"),
    0x3A2A: ("POSTAL_CODE", "STRING"),
    0x3A2B: ("POST_OFFICE_BOX", "STRING"),
    0x3A2C: ("TELEX_NUMBER", "STRING"),
    0x3A2D: ("ISDN_NUMBER", "STRING"),
    0x3A2E: ("ASSISTANT_TELEPHONE_NUMBER", "STRING"),
    0x3A2F: ("HOME2_TELEPHONE_NUMBER", "STRING"),
    0x3A30: ("ASSISTANT", "STRING"),
    0x3A40: ("SEND_RICH_INFO", "BOOLEAN"),
    0x3A41: ("WEDDING_ANNIVERSARY", "SYSTIME"),
    0x3A42: ("BIRTHDAY", "SYSTIME"),
    0x3A43: ("HOBBIES", "STRING"),
    0x3A44: ("MIDDLE_NAME", "STRING"),
    0x3A45: ("DISPLAY_NAME_PREFIX", "STRING"),
    0x3A46: ("PROFESSION", "STRING"),
    0x3A47: ("PREFERRED_BY_NAME", "STRING"),
    0x3A48: ("SPOUSE_NAME", "STRING"),
    0x3A49: ("COMPUTER_NETWORK_NAME", "STRING"),
    0x3A4A: ("CUSTOMER_ID", "STRING"),
    0x3A4B: ("TTYTDD_PHONE_NUMBER", "STRING"),
    0x3A4C: ("FTP_SITE", "STRING"),
    0x3A4D: ("GENDER", "I2"),
    0x3A4E: ("MANAGER_NAME", "STRING"),
    0x3A4F: ("NICKNAME", "STRING"),
    0x3A50: ("PERSONAL_HOME_PAGE", "STRING"),
    0x3A51: ("BUSINESS_HOME_PAGE", "STRING"),
    0x3A52: ("CONTACT_VERSION", "CLSID"),
    0x3A53: ("CONTACT_ENTRYIDS", "MV_BINARY"),
    0x3A54: ("CONTACT_ADDRTYPES", "MV_STRING"),
    0x3A55: ("CONTACT_DEFAULT_ADDRESS_INDEX", "I4"),
    0x3A56: ("CONTACT_EMAIL_ADDRESSES", "MV_STRING"),
    0x3A57: ("COMPANY_MAIN_PHONE_NUMBER", "STRING"),
    0x3A58: ("CHILDRENS_NAMES", "MV_STRING"),
    0x3A59: ("HOME_ADDRESS_CITY", "STRING"),
    0x3A5A: ("HOME_ADDRESS_COUNTRY", "STRING"),
    0x3A5B: ("HOME_ADDRESS_POSTAL_CODE", "STRING"),
    0x3A5C: ("HOME_ADDRESS_STATE_OR_PROVINCE", "STRING"),
    0x3A5D: ("HOME_ADDRESS_STREET", "STRING"),
    0x3A5E: ("HOME_ADDRESS_POST_OFFICE_BOX", "STRING"),
    0x3A5F: ("OTHER_ADDRESS_CITY", "STRING"),
    0x3A60: ("OTHER_ADDRESS_COUNTRY", "STRING"),
    0x3A61: ("OTHER_ADDRESS_POSTAL_CODE", "STRING"),
    0x3A62: ("OTHER_ADDRESS_STATE_OR_PROVINCE", "STRING"),
    0x3A63: ("OTHER_ADDRESS_STREET", "STRING"),
    0x3A64: ("OTHER_ADDRESS_POST_OFFICE_BOX", "STRING"),
    0x3D00: ("STORE_PROVIDERS", "BINARY"),
    0x3D01: ("AB_PROVIDERS", "BINARY"),
    0x3D02: ("TRANSPORT_PROVIDERS", "BINARY"),
    0x3D04: ("DEFAULT_PROFILE", "BOOLEAN"),
    0x3D05: ("AB_SEARCH_PATH", "MV_BINARY"),
    0x3D06: ("AB_DEFAULT_DIR", "BINARY"),
    0x3D07: ("AB_DEFAULT_PAB", "BINARY"),
    0x3D09: ("SERVICE_NAME", "STRING"),
    0x3D0A: ("SERVICE_DLL_NAME", "STRING"),
    0x3D0B: ("SERVICE_ENTRY_NAME", "STRING"),
    0x3D0C: ("SERVICE_UID", "BINARY"),
    0x3D0D: ("SERVICE_EXTRA_UIDS", "BINARY"),
    0x3D0E: ("SERVICES", "BINARY"),
    0x3D0F: ("SERVICE_SUPPORT_FILES", "MV_STRING"),
    0x3D10: ("SERVICE_DELETE_FILES", "MV_STRING"),
    0x3D11: ("AB_SEARCH_PATH_UPDATE", "BINARY"),
    0x3D12: ("PROFILE_NAME", "STRING"),
    0x3E00: ("IDENTITY_DISPLAY", "STRING"),
    0x3E01: ("IDENTITY_ENTRYID", "BINARY"),
    0x3E02: ("RESOURCE_METHODS", "I4"),
    # Service provider type
    0x3E03: ("RESOURCE_TYPE", "I4"),
    0x3E04: ("STATUS_CODE", "I4"),
    0x3E05: ("IDENTITY_SEARCH_KEY", "BINARY"),
    0x3E06: ("OWN_STORE_ENTRYID", "BINARY"),
    0x3E07: ("RESOURCE_PATH", "STRING"),
    0x3E08: ("STATUS_STRING", "STRING"),
    0x3E09: ("X400_DEFERRED_DELIVERY_CANCEL", "BOOLEAN"),
    0x3E0A: ("HEADER_FOLDER_ENTRYID", "BINARY"),
    0x3E0B: ("REMOTE_PROGRESS", "I4"),
    0x3E0C: ("REMOTE_PROGRESS_TEXT", "STRING"),
    0x3E0D: ("REMOTE_VALIDATE_OK", "BOOLEAN"),
    0x3F00: ("CONTROL_FLAGS", "I4"),
    0x3F01: ("CONTROL_STRUCTURE", "BINARY"),
    0x3F02: ("CONTROL_TYPE", "I4"),
    0x3F03: ("DELTAX", "I4"),
    0x3F04: ("DELTAY", "I4"),
    0x3F05: ("XPOS", "I4"),
    0x3F06: ("YPOS", "I4"),
    0x3F07: ("CONTROL_ID", "BINARY"),
    0x3F08: ("INITIAL_DETAILS_PANE", "I4"),
}


code_pages = {
    # Microsoft code page id: python codec name
    437: "cp437",
    850: "cp850",
    852: "cp852",
    936: "gb2312",
    1250: "cp1250",
    1251: "cp1251",
    1252: "cp1252",
    1253: "cp1253",
    1254: "cp1254",
    1255: "cp1255",
    1256: "cp1256",
    1257: "cp1257",
    1258: "cp1258",
    20127: "ascii",
    20866: "koi8-r",
    21866: "koi8-u",
    28591: "iso8859_1",
    28592: "iso8859_2",
    28593: "iso8859_3",
    28594: "iso8859_4",
    28595: "iso8859_5",
    28596: "iso8859_6",
    28597: "iso8859_7",
    28598: "iso8859_8",
    28599: "iso8859_9",
    28603: "iso8859_13",
    28605: "iso8859_15",
    65001: "utf-8",
}
