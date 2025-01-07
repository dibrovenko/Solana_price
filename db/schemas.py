import json
from datetime import datetime, timezone
from pydantic import BaseModel, model_validator
from typing import Optional


class SolanaDTO(BaseModel):
    price: float
    open: float
    close: float
    low: float
    high: float
    volume: float

    time: datetime

    # Валидатор для обработки price
    @model_validator(mode='before')
    def correct_time(cls, values):
        values['time'] = datetime.fromtimestamp(values['time'], tz=timezone.utc).replace(tzinfo=None)
        return values

    # Валидатор для обработки price
    @model_validator(mode='before')
    def set_price(cls, values):
        values["price"] = (values["open"] + values["close"]) / 2
        return values

    class Config:
        # Config for supporting types like Enum and UUIDs.
        use_enum_values = True
        from_attributes = True




