COOKIE = 'eyJtb25leSI6MTB9.Xte3Tw.SNcBb_nBfK-vYjEzjlfARK92tXE'

encoded_session = 'eyJtb25leSI6MTB9'
encoded_timestamp = 'Xte3Tw'
encoded_hash_secret = 'SNcBb_nBfK-vYjEzjlfARK92tXE'

session_data = {
    'money': 10
}

import base64
import hashlib
from itsdangerous import URLSafeTimedSerializer, TimestampSigner
from flask.sessions import TaggedJSONSerializer, BadSignature, session_json_serializer

signer_1 = URLSafeTimedSerializer(
    'secret-key', salt='cookie-session',
    serializer=session_json_serializer,
    signer_kwargs={'key_derivation': 'hmac', 'digest_method': hashlib.sha512}
)

signer_2 = URLSafeTimedSerializer(
    'secret-key', salt='cookie-session',
    serializer=session_json_serializer,
    signer_kwargs={'key_derivation': 'hmac', 'digest_method': hashlib.sha1}
)

signer_3 = URLSafeTimedSerializer(
    'secret-key', salt='cookie-session',
    serializer=TaggedJSONSerializer(),
    signer_kwargs={'key_derivation': 'hmac', 'digest_method': hashlib.sha512}
)

signer_4 = URLSafeTimedSerializer(
    'secret-key', salt='cookie-session',
    serializer=TaggedJSONSerializer(),
    signer_kwargs={'key_derivation': 'hmac', 'digest_method': hashlib.sha1}
)

signers = (
    signer_1,
    signer_2,
    signer_3,
    signer_4,
)

def crack_secret(secret):
    for id, signer in enumerate(signers):
        try:
            serializer = URLSafeTimedSerializer(
                secret_key=secret,
                salt='cookie-session',
                serializer=TaggedJSONSerializer(),
                signer=TimestampSigner,
                signer_kwargs={
                    'key_derivation': 'hmac',
                    'digest_method': hashlib.sha1
                }
            ).loads(COOKIE)

            print(f"Secret key found: {secret}")

        except BadSignature:
            print(f"Bad secret - {id+1}")



import flask_unsign_wordlist
def main():
    wordlist = flask_unsign_wordlist.get('all')
    print(wordlist)


if __name__ == '__main__':
    main()
