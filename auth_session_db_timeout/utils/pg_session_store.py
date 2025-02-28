import logging
import psycopg2

from odoo.addons.session_db.pg_session_store import PGSessionStore
import odoo

_logger = logging.getLogger(__name__)

lock = None
if odoo.evented:
    import gevent.lock

    lock = gevent.lock.RLock()
elif odoo.tools.config["workers"] == 0:
    import threading

    lock = threading.RLock()


def with_lock(func):
    def wrapper(*args, **kwargs):
        try:
            if lock is not None:
                lock.acquire()
            return func(*args, **kwargs)
        finally:
            if lock is not None:
                lock.release()

    return wrapper


def with_cursor(func):
    def wrapper(self, *args, **kwargs):
        tries = 0
        while True:
            tries += 1
            try:
                self._ensure_connection()
                return func(self, *args, **kwargs)
            except (psycopg2.InterfaceError, psycopg2.OperationalError):
                self._close_connection()
                if tries > 4:
                    _logger.warning(
                        "session_db operation try %s/5 failed, aborting", tries
                    )
                    raise
                _logger.info("session_db operation try %s/5 failed, retrying", tries)

    return wrapper


class PGSessionStoreExtended(PGSessionStore):
    @with_lock
    @with_cursor
    def get_write_date(self, sid):
        """
        Retrieve the most recent write_date for a given session ID.
        """
        self._cr.execute(
            """
            SELECT write_date FROM http_sessions
            WHERE sid=%s
            ORDER BY write_date DESC
            LIMIT 1
            """,
            (sid,),
        )
        result = self._cr.fetchone()
        return result[0] if result else None
