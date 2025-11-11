import vt

from .emailrep import EmailRep  # noqa: F401
from .spamassasin import SpamAssassin  # noqa: F401
from .urlscan import UrlScan  # noqa: F401

VirusTotal = vt.Client
