from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class Transaction(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    id: int
    accountId: int
    type: Literal[
        "Credit",
        "Debit"
    ]
    date: datetime
    amount: float
    description: str