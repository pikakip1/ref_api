import uuid
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


class ReferralCode(Base):
    __tablename__ = 'referral_code'

    duration: Mapped[datetime] = mapped_column(
        default=datetime.now() + timedelta(days=30),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    number_of_registered_referrals: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
    user: Mapped['User'] = relationship(back_populates='referral_code')
