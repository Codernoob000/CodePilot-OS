"""Stable public error response contract."""

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Safe error envelope returned by the API."""

    code: str
    message: str
    request_id: str | None = None
    retryable: bool = False
