# -*- encoding: utf-8 -*-

import os
import hashlib
import hmac

class Auth:
    @staticmethod
    def github(headers, raw_payload):
        received_sig = to_bytes(headers.get('X-Hub-Signature'))

        secret = to_bytes(os.getenv('WEBHOOK_SECRET_TOKEN'))
        h = hmac.new(secret, raw_payload, hashlib.sha1).hexdigest()
        correct_sig = b'sha1=' + to_bytes(h)

        try:
            return hmac.compare_digest(received_sig, correct_sig)
        except:
            return False


    @staticmethod
    def gitlab(headers, raw_payload):
        received_token = to_bytes(headers.get('X-Gitlab-Token'))
        secret = to_bytes(os.getenv('WEBHOOK_SECRET_TOKEN'))

        try:
            return hmac.compare_digest(secret, received_token)
        except:
            return False



text_type = type('')

def to_bytes(s):
    if isinstance(s, text_type):
        return bytes(s.encode('utf-8'))
    return s
