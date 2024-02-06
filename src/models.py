import uuid
from datetime import datetime, timedelta

from pydantic import EmailStr
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = 'user'

    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    referral_code: Mapped['ReferralCode'] = relationship(
        'ReferralCode',
        uselist=False,
        back_populates='user',
    )


class ReferralCode(Base):
    __tablename__ = 'referral_code'

    duration: Mapped[datetime] = mapped_column(
        default=datetime.now() + timedelta(days=30),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    number_of_registered_referrals: Mapped[int] = mapped_column(default=0)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['User'] = relationship('User', back_populates='referral_code')
