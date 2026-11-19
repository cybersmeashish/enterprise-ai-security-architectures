"""Ephemeral opaque credentials for the local demo, not an enterprise IdP."""
from dataclasses import dataclass
import hashlib
import secrets
import threading
from .contracts import Denied


@dataclass(frozen=True)
class Principal:
    subject: str
    tenant: str
    use_cases: tuple
    scopes: tuple
    role: str = "workload"


class Identity:
    def __init__(self, clock):
        self.clock = clock
        self._records = {}
        self._lock = threading.RLock()

    def issue(self, principal, ttl=300):
        token = secrets.token_urlsafe(32)
        with self._lock:
            self._records[hashlib.sha256(token.encode()).digest()] = (
                principal, self.clock() + ttl, False)
        return token

    def resolve(self, token):
        if not isinstance(token, str) or not 20 <= len(token) <= 256:
            raise Denied("invalid_credential", 401)
        with self._lock:
            record = self._records.get(hashlib.sha256(token.encode()).digest())
        if record is None or record[2] or self.clock() >= record[1]:
            raise Denied("invalid_credential", 401)
        return record[0]

    def revoke(self, token):
        with self._lock:
            key = hashlib.sha256(token.encode()).digest()
            p, expires, _ = self._records[key]
            self._records[key] = (p, expires, True)
