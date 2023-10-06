from base64 import urlsafe_b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from pydantic import BaseModel


class JWK(BaseModel):
    alg: str
    e: str
    kid: str
    kty: str
    n: str
    use: str


def ensure_base64_padding(data: str) -> str:
    pad_needed = 4 - len(data) % 4
    return data + "=" * pad_needed


def jwk_to_pem(jwk: JWK) -> bytes:
    e_padded = ensure_base64_padding(jwk.e)
    n_padded = ensure_base64_padding(jwk.n)

    public_numbers = rsa.RSAPublicNumbers(
        e=int.from_bytes(urlsafe_b64decode(e_padded), "big"),
        n=int.from_bytes(urlsafe_b64decode(n_padded), "big"),
    )
    public_key = public_numbers.public_key(default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem
