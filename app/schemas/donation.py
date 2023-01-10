from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, PositiveInt


class DonationCreateSchema(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extras = Extra.forbid
        schema_extra = {
            'example': {
                'comment': 'А я люблю собак, но все равно пожертвую',
                'full_amount': 25
            }
        }


class DonationDBSchema(DonationCreateSchema):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationsDBSchema(DonationDBSchema):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
