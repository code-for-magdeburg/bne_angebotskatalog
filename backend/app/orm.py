# ORM models (SQLAlchemy) corresponding to tables
from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, declarative_base, relationship

Base = declarative_base()


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    address_recipient: Mapped[Optional[str]] = sa.Column(sa.Text)
    address_recipient_addition: Mapped[Optional[str]] = sa.Column(sa.Text)
    address_street: Mapped[str] = sa.Column(sa.Text, nullable=False)
    address_city: Mapped[str] = sa.Column(sa.Text, nullable=False)
    address_zip_code: Mapped[str] = sa.Column(sa.Text, nullable=False)
    address_accessible: Mapped[bool] = sa.Column(
        sa.Boolean,
        nullable=False,
    )

    __table_args__ = (
        sa.CheckConstraint("address_accessible IN (0, 1)"),
    )


class Link(Base):
    __tablename__ = "link"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    link_type: Mapped[str] = sa.Column(sa.Text, nullable=False)
    value: Mapped[str] = sa.Column(sa.Text, nullable=False)

    __table_args__ = (
        sa.CheckConstraint(
            "link_type IN ('website', 'instagram', 'mastodon', 'facebook', 'twitter')"
        ),
        sa.CheckConstraint("length(trim(value)) > 0"),
        sa.UniqueConstraint("link_type", "value"),
    )


class Institution(Base):
    __tablename__ = "institution"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_type: Mapped[str] = sa.Column(sa.Text, nullable=False)
    name: Mapped[str] = sa.Column(sa.Text, nullable=False)
    description: Mapped[str] = sa.Column(sa.Text, nullable=False)
    address_id: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    logo_url: Mapped[Optional[str]] = sa.Column(sa.Text)
    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer)

    __table_args__ = (
        sa.CheckConstraint(
            "institution_type IN ("
            "'kita_vorschule', "
            "'grundschule', "
            "'schule', "
            "'universität', "
            "'verein', "
            "'privates_unternehmen', "
            "'städtisches_unternehmen', "
            "'stiftung', "
            "'städtische_organisation', "
            "'amt', "
            "'ministerium', "
            "'pflegeheim'"
            ")"
        ),
        sa.CheckConstraint("length(trim(name)) > 0"),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["address.id"],
            onupdate="CASCADE",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["link.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
    )

    address = relationship(
        "Address",
        backref="institution",
        uselist=False,
    )
    link = relationship(
        "Link",
        backref="institution",
        uselist=False,
    )


class Agent(Base):
    __tablename__ = "agent"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_id: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    first_name: Mapped[str] = sa.Column(sa.Text, nullable=False)
    last_name: Mapped[str] = sa.Column(sa.Text, nullable=False)
    phone: Mapped[Optional[str]] = sa.Column(sa.Text)
    email: Mapped[str] = sa.Column(sa.Text, nullable=False)
    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer)

    __table_args__ = (
        sa.CheckConstraint("length(trim(first_name)) > 0"),
        sa.CheckConstraint("length(trim(last_name)) > 0"),
        sa.CheckConstraint("length(trim(email)) > 0"),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institution.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["link.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
    )

    institution = relationship(
        "Institution",
        backref="agents",
    )
    link = relationship(
        "Link",
        backref="agent",
        uselist=False,
    )


class Offer(Base):
    __tablename__ = "offer"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True)
    institution_id: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    offer_type: Mapped[str] = sa.Column(sa.Text, nullable=False)
    name: Mapped[str] = sa.Column(sa.Text, nullable=False)
    agent_id: Mapped[Optional[int]] = sa.Column(sa.Integer)
    image_url: Mapped[Optional[str]] = sa.Column(sa.Text)
    description: Mapped[str] = sa.Column(sa.Text, nullable=False)
    address_id: Mapped[Optional[int]] = sa.Column(sa.Integer)

    timeframe_duration_minutes: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
    )
    timeframe_recurrence_interval: Mapped[Optional[int]] = sa.Column(
        sa.Integer,
    )
    timeframe_recurrence_unit: Mapped[Optional[str]] = sa.Column(
        sa.Text,
    )
    timeframe_note: Mapped[Optional[str]] = sa.Column(sa.Text)

    cost_type: Mapped[str] = sa.Column(sa.Text, nullable=False)
    cost_amount: Mapped[Optional[float]] = sa.Column(sa.Float)
    cost_currency: Mapped[str] = sa.Column(
        sa.Text,
        nullable=False,
        default="EUR",
        server_default="EUR",
    )
    cost_unit: Mapped[Optional[str]] = sa.Column(sa.Text)
    cost_note: Mapped[Optional[str]] = sa.Column(sa.Text)

    min_participants: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
    )
    max_participants: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
    )

    link_id: Mapped[Optional[int]] = sa.Column(sa.Integer)

    __table_args__ = (
        sa.CheckConstraint(
            "offer_type IN ("
            "'workshop', "
            "'exkursion', "
            "'mentoring', "
            "'podiumsdiskussion', "
            "'ausstellung', "
            "'infostand', "
            "'projekttag', "
            "'projektwoche', "
            "'kino', "
            "'fortbildung', "
            "'ausleihbares_lernmaterial', "
            "'beratung'"
            ")"
        ),
        sa.CheckConstraint("length(trim(name)) > 0"),
        sa.CheckConstraint("timeframe_duration_minutes > 0"),
        sa.CheckConstraint(
            "timeframe_recurrence_interval IS NULL "
            "OR timeframe_recurrence_interval > 0"
        ),
        sa.CheckConstraint(
            "timeframe_recurrence_unit IN ('woche', 'monat', 'jahr')"
        ),
        sa.CheckConstraint(
            "("
            "timeframe_recurrence_interval IS NULL "
            "AND timeframe_recurrence_unit IS NULL"
            ") OR ("
            "timeframe_recurrence_interval IS NOT NULL "
            "AND timeframe_recurrence_unit IS NOT NULL"
            ")"
        ),
        sa.CheckConstraint(
            "cost_type IN ('free', 'paid')"
        ),
        sa.CheckConstraint(
            "cost_amount IS NULL OR cost_amount >= 0"
        ),
        sa.CheckConstraint(
            "cost_currency = 'EUR'"
        ),
        sa.CheckConstraint("min_participants > 0"),
        sa.CheckConstraint(
            "max_participants >= min_participants"
        ),
        sa.CheckConstraint(
            "("
            "cost_type = 'free' "
            "AND (cost_amount IS NULL OR cost_amount = 0)"
            ") OR ("
            "cost_type = 'paid' "
            "AND cost_amount IS NOT NULL "
            "AND cost_amount > 0"
            ")"
        ),
        sa.ForeignKeyConstraint(
            ["institution_id"],
            ["institution.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agent.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["address_id"],
            ["address.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["link.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
    )

    institution = relationship(
        "Institution",
        backref="offers",
    )
    agent = relationship(
        "Agent",
        backref="offers",
        uselist=False,
    )
    address = relationship(
        "Address",
        backref="offers",
        uselist=False,
    )
    link = relationship(
        "Link",
        backref="offer_links",
        uselist=False,
    )


class OfferLocation(Base):
    __tablename__ = "offer_location"

    offer_id: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
        primary_key=True,
    )
    location: Mapped[str] = sa.Column(
        sa.Text,
        nullable=False,
        primary_key=True,
    )

    __table_args__ = (
        sa.CheckConstraint(
            "location IN ('bei_euch', 'bei_uns', 'dritter_ort', 'online')"
        ),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["offer.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class OfferTargetGroup(Base):
    __tablename__ = "offer_target_group"

    offer_id: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
        primary_key=True,
    )
    target_group: Mapped[str] = sa.Column(
        sa.Text,
        nullable=False,
        primary_key=True,
    )

    __table_args__ = (
        sa.CheckConstraint(
            "length(trim(target_group)) > 0"
        ),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["offer.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )


class OfferSdg(Base):
    __tablename__ = "offer_sdg"

    offer_id: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
        primary_key=True,
    )
    sdg: Mapped[int] = sa.Column(
        sa.Integer,
        nullable=False,
        primary_key=True,
    )

    __table_args__ = (
        sa.CheckConstraint("sdg BETWEEN 1 AND 17"),
        sa.ForeignKeyConstraint(
            ["offer_id"],
            ["offer.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
