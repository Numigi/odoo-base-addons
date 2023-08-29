# © 2023 Numigi (tm) and all its contributors (https://bit.ly/numigiens)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
import time

_logger = logging.getLogger(__name__)

from odoo.addons.session_redis.session import RedisSessionStore



class RedisSessionStoreTimeout(RedisSessionStore):
    """ SessionStore that saves session to redis """

    def __init__(self, redis, session_class=None, prefix='', expiration=None, anon_expiration=None):
        super(RedisSessionStoreTimeout, self).__init__(redis=redis, session_class=session_class,
                                                       prefix=prefix, expiration=expiration,
                                                       anon_expiration=anon_expiration)
        self.redis = redis
    

    def get_activity_time(self, session):
        session_key = self.build_key(session.sid)
        current_time = time.time()
        get_session = self.redis.hget(session_key + ':info', b'updated_at')
        if get_session:
            info = get_session.decode('utf-8')
            updated_at = float(info)
            return updated_at
        return current_time
    
    def set_activity_time(self, session):
        session_key = self.build_key(session.sid)
        current_time = time.time()
        self.redis.hset(session_key + ':info', 'updated_at', current_time)
        return True
