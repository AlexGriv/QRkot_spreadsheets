from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt

from ..services.constants import MIN_LENGTH, MAX_LENGTH


class CharityProjectCreateSchema(BaseModel):
    name: str = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Рыжий котик',
                'description': 'На корм',
                'full_amount': 1100
            }
        }


class CharityProjectDBSchema(CharityProjectCreateSchema):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdateSchema(BaseModel):
    name: Optional[str] = Field(min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: Optional[str] = Field(min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid
        schema_extra = {
            'example': {
                'name': 'Черный котик',
                'description': 'Новые игрушки',
                'full_amount': 700
            }
        }
