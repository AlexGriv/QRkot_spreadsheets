from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract_models import AbstractModel


class Donation(AbstractModel):
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))
