"""System health response contract."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Process-level health response used by deployment probes."""

    status: Literal["ok"]
    service: str
    version: str
    environment: str
    request_id: str | None = None
