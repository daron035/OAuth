import base64
import hashlib
import secrets

from dataclasses import dataclass, field

from src.domain.common.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class PKCEPair(BaseValueObject):
    code_verifier: str = field(init=False)
    code_challenge: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "code_verifier", self._generate_code_verifier())
        object.__setattr__(self, "code_challenge", self._generate_code_challenge(self.code_verifier))

    @staticmethod
    def _generate_code_verifier() -> str:
        return secrets.token_urlsafe(64)

    @staticmethod
    def _generate_code_challenge(code_verifier: str) -> str:
        digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
