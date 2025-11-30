from jwcrypto import jwk
from app.core import config

_KID = config.JWT_KID
_PRIV = jwk.JWK.generate(kty="RSA", size=2048)
_PUB = _PRIV.export_public(as_dict=True)


def jwks() -> dict:
    return {"keys": [{**_PUB, "kid": _KID, "alg": "RS256", "use": "sig"}]}
