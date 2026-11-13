"""
Django-E-Mail-Backend für Microsoft Graph (sendMail mit App-Berechtigung).

Die Website meldet sich mit einer eigenen App-Identität (Client Credentials)
bei Microsoft an und verschickt Mails als GRAPH_SENDER (info@datalization.ch).
Welche Postfächer die App benutzen darf, ist in Exchange Online per
"RBAC for Applications" eingeschränkt (Scope "Nur info-Postfach").

Benötigte Settings (aus Umgebungsvariablen):
    GRAPH_TENANT_ID, GRAPH_CLIENT_ID, GRAPH_CLIENT_SECRET, GRAPH_SENDER

Keine Zusatzpakete nötig – nur Python-Standardbibliothek.
"""

import base64
import json
import logging
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from email.mime.base import MIMEBase
from email.utils import parseaddr

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

logger = logging.getLogger(__name__)

TOKEN_URL = "https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token"
SEND_URL = "https://graph.microsoft.com/v1.0/users/{sender}/sendMail"
SCOPE = "https://graph.microsoft.com/.default"

# Token wird prozessweit zwischengespeichert (gilt ca. 60 Minuten).
_token_lock = threading.Lock()
_token_cache = {"value": None, "expires_at": 0.0}


class GraphEmailBackend(BaseEmailBackend):
    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently, **kwargs)
        self.tenant_id = getattr(settings, "GRAPH_TENANT_ID", "")
        self.client_id = getattr(settings, "GRAPH_CLIENT_ID", "")
        self.client_secret = getattr(settings, "GRAPH_CLIENT_SECRET", "")
        self.sender = getattr(settings, "GRAPH_SENDER", "")
        self.timeout = getattr(settings, "EMAIL_TIMEOUT", None) or 15

    # ------------------------------------------------------------------ #
    # Öffentliche API (wird von Django aufgerufen)
    # ------------------------------------------------------------------ #
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        missing = [
            name
            for name, value in (
                ("GRAPH_TENANT_ID", self.tenant_id),
                ("GRAPH_CLIENT_ID", self.client_id),
                ("GRAPH_CLIENT_SECRET", self.client_secret),
                ("GRAPH_SENDER", self.sender),
            )
            if not value
        ]
        if missing:
            error = RuntimeError(f"Graph-Mail nicht konfiguriert, fehlt: {', '.join(missing)}")
            if self.fail_silently:
                logger.error(str(error))
                return 0
            raise error

        sent = 0
        for message in email_messages:
            if not message.recipients():
                continue
            try:
                self._send(message)
                sent += 1
            except Exception:
                logger.exception("Graph-Mailversand fehlgeschlagen (Betreff: %s)", message.subject)
                if not self.fail_silently:
                    raise
        return sent

    # ------------------------------------------------------------------ #
    # Interna
    # ------------------------------------------------------------------ #
    def _get_token(self):
        with _token_lock:
            if _token_cache["value"] and time.time() < _token_cache["expires_at"] - 60:
                return _token_cache["value"]

            data = urllib.parse.urlencode(
                {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "scope": SCOPE,
                    "grant_type": "client_credentials",
                }
            ).encode()
            request = urllib.request.Request(
                TOKEN_URL.format(tenant=self.tenant_id), data=data, method="POST"
            )
            payload = self._open(request)
            _token_cache["value"] = payload["access_token"]
            _token_cache["expires_at"] = time.time() + int(payload.get("expires_in", 3599))
            return _token_cache["value"]

    def _send(self, message):
        body = json.dumps(self._build_payload(message)).encode("utf-8")
        request = urllib.request.Request(
            SEND_URL.format(sender=urllib.parse.quote(self.sender)),
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bearer {self._get_token()}",
                "Content-Type": "application/json",
            },
        )
        self._open(request, expect_json=False)

    def _open(self, request, expect_json=True):
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise RuntimeError(f"Microsoft Graph HTTP {exc.code}: {detail}") from None
        return json.loads(raw) if expect_json and raw else None

    def _build_payload(self, message):
        content_type, content = "Text", message.body
        if getattr(message, "content_subtype", "plain") == "html":
            content_type = "HTML"
        for alt_content, mimetype in getattr(message, "alternatives", []) or []:
            if mimetype == "text/html":
                content_type, content = "HTML", alt_content
                break

        graph_message = {
            "subject": message.subject,
            "body": {"contentType": content_type, "content": content},
            "toRecipients": _recipients(message.to),
        }
        if message.cc:
            graph_message["ccRecipients"] = _recipients(message.cc)
        if message.bcc:
            graph_message["bccRecipients"] = _recipients(message.bcc)
        if message.reply_to:
            graph_message["replyTo"] = _recipients(message.reply_to)

        attachments = [_attachment(item) for item in message.attachments]
        attachments = [a for a in attachments if a]
        if attachments:
            graph_message["attachments"] = attachments

        return {"message": graph_message, "saveToSentItems": True}


def _recipients(addresses):
    result = []
    for entry in addresses:
        name, address = parseaddr(entry)
        email_address = {"address": address or entry}
        if name:
            email_address["name"] = name
        result.append({"emailAddress": email_address})
    return result


def _attachment(item):
    if isinstance(item, MIMEBase):
        filename = item.get_filename() or "anhang"
        content = item.get_payload(decode=True) or b""
        mimetype = item.get_content_type()
    else:
        filename, content, mimetype = item
        if isinstance(content, str):
            content = content.encode("utf-8")
    return {
        "@odata.type": "#microsoft.graph.fileAttachment",
        "name": filename,
        "contentType": mimetype or "application/octet-stream",
        "contentBytes": base64.b64encode(content).decode("ascii"),
    }
