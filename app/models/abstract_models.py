from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class AbstractModel(Base):
    """Абстрактная модель для CharityProject & Donation."""
    __abstract__ = True

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return (
            f'full_amount: {self.full_amount}, '
            f'invested_amount: {self.invested_amount}, '
            f'create_date: {self.create_date}'
        )
