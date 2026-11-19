"""Transactional local reference state. Shared HA state is a separate target design."""
from contextlib import contextmanager
import hashlib
import json
import secrets
import sqlite3
import threading
from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .contracts import Denied, canonical


class Store:
    def __init__(self, path, clock, encryption_key=None):
        self.clock = clock
        # The demo uses an ephemeral process key; a restored store needs the same
        # separately protected key to replay encrypted response records.
        self.cipher = AESGCM(encryption_key or AESGCM.generate_key(bit_length=256))
        self.lock = threading.RLock()
        self.db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.db.execute("PRAGMA busy_timeout=3000")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS budgets(tenant TEXT PRIMARY KEY, spent INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS rates(tenant TEXT, minute INTEGER, count INTEGER,
                                       PRIMARY KEY(tenant, minute));
        CREATE TABLE IF NOT EXISTS requests(key TEXT PRIMARY KEY, fingerprint TEXT,
                                           state TEXT, response TEXT, expires INTEGER);
        CREATE TABLE IF NOT EXISTS approvals(handle TEXT PRIMARY KEY, tenant TEXT,
                        requester TEXT, reviewer TEXT, action TEXT, expires INTEGER, used INTEGER);
        CREATE TABLE IF NOT EXISTS actions(id INTEGER PRIMARY KEY, tenant TEXT,
                                          subject TEXT, action TEXT);
        CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, event TEXT,
                                        previous TEXT, hash TEXT);
        CREATE TABLE IF NOT EXISTS revisions(site TEXT PRIMARY KEY, revision INTEGER, digest TEXT);
        """)

    @contextmanager
    def transaction(self):
        with self.lock:
            self.db.execute("BEGIN IMMEDIATE")
            try:
                yield self.db
                self.db.execute("COMMIT")
            except BaseException:
                self.db.execute("ROLLBACK")
                raise

    def accept_revision(self, site, revision, policy_digest="unspecified"):
        with self.transaction() as db:
            row = db.execute("SELECT revision,digest FROM revisions WHERE site=?", (site,)).fetchone()
            if row and revision < row[0]:
                raise Denied("policy_rollback")
            if row and revision == row[0] and policy_digest != row[1]:
                raise Denied("policy_revision_conflict")
            db.execute("INSERT OR REPLACE INTO revisions VALUES (?,?,?)", (site, revision, policy_digest))

    def claim(self, key, fingerprint):
        now = int(self.clock())
        with self.transaction() as db:
            # A running request remains blocked until operator recovery; expiration
            # alone must not cause duplicate upstream execution.
            db.execute("DELETE FROM requests WHERE expires<=? AND state='complete'", (now,))
            row = db.execute("SELECT fingerprint,state,response FROM requests WHERE key=?", (key,)).fetchone()
            if row:
                if row[0] != fingerprint:
                    raise Denied("idempotency_conflict", 409)
                if row[1] == "running":
                    raise Denied("request_in_progress", 409)
                encrypted = bytes.fromhex(row[2])
                try:
                    return json.loads(self.cipher.decrypt(encrypted[:12], encrypted[12:], key.encode()))
                except (InvalidTag, ValueError):
                    raise Denied("cached_response_key_unavailable", 503) from None
            count = db.execute("SELECT COUNT(*) FROM requests").fetchone()[0]
            if count >= 10000:
                raise Denied("idempotency_store_full", 503)
            db.execute("INSERT INTO requests VALUES (?,?, 'running',NULL,?)",
                       (key, fingerprint, now + 30))
        return None

    def finish(self, key, response):
        nonce = secrets.token_bytes(12)
        encrypted = nonce + self.cipher.encrypt(nonce, canonical(response), key.encode())
        with self.transaction() as db:
            db.execute("UPDATE requests SET state='complete',response=?,expires=? WHERE key=?",
                       (encrypted.hex(), int(self.clock()) + 30, key))

    def reserve(self, tenant, credits, budget, rpm):
        minute = int(self.clock()) // 60
        with self.transaction() as db:
            spent = db.execute("SELECT spent FROM budgets WHERE tenant=?", (tenant,)).fetchone()
            spent = spent[0] if spent else 0
            rate = db.execute("SELECT count FROM rates WHERE tenant=? AND minute=?",
                              (tenant, minute)).fetchone()
            count = rate[0] if rate else 0
            if spent + credits > budget:
                raise Denied("budget_exhausted", 429)
            if count >= rpm:
                raise Denied("rate_exceeded", 429)
            db.execute("INSERT OR REPLACE INTO budgets VALUES (?,?)", (tenant, spent + credits))
            db.execute("INSERT OR REPLACE INTO rates VALUES (?,?,?)", (tenant, minute, count + 1))
            db.execute("DELETE FROM rates WHERE minute<?", (minute - 2,))

    def spent(self, tenant):
        with self.lock:
            row = self.db.execute("SELECT spent FROM budgets WHERE tenant=?", (tenant,)).fetchone()
        return row[0] if row else 0

    def approve(self, principal, requester, action):
        handle = secrets.token_urlsafe(32)
        key = hashlib.sha256(handle.encode()).hexdigest()
        with self.transaction() as db:
            db.execute("DELETE FROM approvals WHERE expires<=?", (int(self.clock()),))
            if db.execute("SELECT COUNT(*) FROM approvals").fetchone()[0] >= 10000:
                raise Denied("approval_store_full", 503)
            db.execute("INSERT INTO approvals VALUES (?,?,?,?,?,?,0)",
                       (key, principal.tenant, requester, principal.subject, action,
                        int(self.clock()) + 120))
        return handle

    def execute_action(self, principal, action, handles):
        if len(handles) != 2 or len(set(handles)) != 2:
            raise Denied("two_approvals_required")
        keys = [hashlib.sha256(h.encode()).hexdigest() for h in handles]
        with self.transaction() as db:
            reviewers = []
            for key in keys:
                row = db.execute("SELECT tenant,requester,reviewer,action,expires,used FROM approvals "
                                 "WHERE handle=?", (key,)).fetchone()
                if (not row or row[0] != principal.tenant or row[1] != principal.subject
                        or row[3] != action or row[4] <= self.clock() or row[5]
                        or row[2] == principal.subject):
                    raise Denied("invalid_action_approval")
                reviewers.append(row[2])
            if len(set(reviewers)) != 2:
                raise Denied("distinct_reviewers_required")
            for key in keys:
                db.execute("UPDATE approvals SET used=1 WHERE handle=?", (key,))
            cur = db.execute("INSERT INTO actions(tenant,subject,action) VALUES (?,?,?)",
                             (principal.tenant, principal.subject, action))
            self._append_audit(db, {"time": int(self.clock()), "event": "synthetic_tool_completed",
                                   "tenant": principal.tenant, "subject": principal.subject,
                                   "action_digest": action, "action_id": cur.lastrowid})
            return cur.lastrowid

    def _append_audit(self, db, event):
        previous = db.execute("SELECT hash FROM audit ORDER BY id DESC LIMIT 1").fetchone()
        previous = previous[0] if previous else "0" * 64
        text = canonical(event).decode()
        checksum = hashlib.sha256(previous.encode() + text.encode()).hexdigest()
        db.execute("INSERT INTO audit(event,previous,hash) VALUES (?,?,?)", (text, previous, checksum))

    def audit(self, event):
        with self.transaction() as db:
            self._append_audit(db, event)

    def audit_rows(self):
        with self.lock:
            return list(self.db.execute("SELECT event,previous,hash FROM audit ORDER BY id"))

    def audit_valid(self):
        previous = "0" * 64
        for event, claimed, checksum in self.audit_rows():
            if claimed != previous or hashlib.sha256(previous.encode() + event.encode()).hexdigest() != checksum:
                return False
            previous = checksum
        return True

    def backup(self, destination):
        with self.lock:
            target = sqlite3.connect(destination)
            try:
                self.db.backup(target)
            finally:
                target.close()

    def close(self):
        self.db.close()
