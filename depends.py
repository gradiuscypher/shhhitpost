from typing import Annotated

from fastapi import Header, HTTPException, Request
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey


class ValidateDiscordRequest:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    async def __call__(
        self,
        request: Request,
        x_signature_ed25519: Annotated[str, Header()] = "",
        x_signature_timestamp: Annotated[str, Header()] = "",
    ) -> None:
        verify_key = VerifyKey(bytes.fromhex(self.public_key))
        body = await request.body()
        decoded_body = body.decode("utf-8")

        try:
            verify_key.verify(
                f"{x_signature_timestamp}{decoded_body}".encode(),
                bytes.fromhex(x_signature_ed25519),
            )
        except BadSignatureError:
            raise HTTPException(status_code=401, detail="invalid request signature")
