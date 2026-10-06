# ORM models (SQLAlchemy) corresponding to tables
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import Mapped

Base = declarative_base()

class Institution(Base):
    __tablename__ = "institution"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_type: Mapped[str] = sa.Column(sa.String, nullable=False)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    description: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("address.id"), nullable=False)
    logo_url: Mapped[Optional[str]] = sa.Column(sa.String)
    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("link.id"))

    address = relationship("Address", backref="institution", uselist=False)
    link = relationship("Link", backref="institution", uselist=False)
    # other relationships omitted for brevity

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    address_recipient: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_recipient_addition: Mapped[Optional[str]] = sa.Column(sa.String)
    address_street: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_city: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_zip_code: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_accessible: Mapped[bool] = sa.Column(sa.Boolean, nullable=False)

class Link(Base):
    __tablename__ = "link"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    link_type: Mapped[str] = sa.Column(sa.String, nullable=False)
    value: Mapped[str] = sa.Column(sa.String, nullable=False)

class Agent(Base):
    __tablename__ = "agent"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("institution.id"), nullable=False)
    first_name: Mapped[str] = sa.Column(sa.String, nullable=False)
    last_name: Mapped[str] = sa.Column(sa.String, nullable=False)
    phone: Mapped[Optional[str]] = sa.Column(sa.String)
    email: Mapped[str] = sa.Column(sa.String, nullable=False)
    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("link.id"))

    institution = relationship("Institution", backref="agents")
    link = relationship("Link", backref="agent", uselist=False)

class Offer(Base):
    __tablename__ = "offer"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("institution.id"), nullable=False)
    offer_type: Mapped[str] = sa.Column(sa.String, nullable=False)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    image_url: Mapped[Optional[str]] = sa.Column(sa.String)
    description: Mapped[str] = sa.Column(sa.String, nullable=False)
    address_id: Mapped[Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("address.id"))
    timeframe_duration_minutes: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    timeframe_recurrence_interval: Mapped[Optional[int]] = sa.Column(sa.Integer)
    timeframe_recurrence_unit: Mapped[Optional[str]] = sa.Column(sa.String)
    timeframe_note: Mapped[Optional[str]] = sa.Column(sa.String)
    cost_type: Mapped[str] = sa.Column(sa.String, nullable=False)
    cost_amount: Mapped[Optional[float]] = sa.Column(sa.Float)
    cost_currency: Mapped[Optional[str]] = sa.Column(sa.String)
    cost_unit: Mapped[Optional[str]] = sa.Column(sa.String)
    cost_note: Mapped[Optional[str]] = sa.Column(sa.String)
    min_participants: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    max_participants: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer, sa.ForeignKey("link.id"))

    institution = relationship("Institution", backref="offers")
    address = relationship("Address", backref="offers", uselist=False)
    link = relationship("Link", backref="offers", uselist=False)

class OfferLocation(Base):
    __tablename__ = "offer_location"
    offer_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("offer.id"), primary_key=True)
    location: Mapped[str] = sa.Column(sa.String, primary_key=True)

class OfferTargetGroup(Base):
    __tablename__ = "offer_target_group"
    offer_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("offer.id"), primary_key=True)
    target_group: Mapped[str] = sa.Column(sa.String, primary_key=True)

class OfferSdg(Base):
    __tablename__ = "offer_sdg"
    offer_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("offer.id"), primary_key=True)
    sdg: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
