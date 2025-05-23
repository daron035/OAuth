from typing import Literal

from pydantic import BaseModel


class Auth(BaseModel):
    response_type: Literal["code", "token"]
    client_id: str
    redirect_uri: str
    code_challenge: str
    code_challenge_method: Literal["S256", "plain"] = "plain"
    scope: str | None = None
    state: str | None = None
    access_type: str | None = None
    prompt: str | None = None
