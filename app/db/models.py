from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    BigInteger,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    technical_key: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        unique=True,
    )

    category_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    data_overviews: Mapped[list[DataOverview]] = relationship(
        back_populates="category",
    )

    label_proposals: Mapped[list[LabelProposal]] = relationship(
        back_populates="category",
    )


class DataOverview(Base):
    __tablename__ = "data_overview"

    technical_key: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    uuid: Mapped[UUID] = mapped_column(
        PostgresUUID(as_uuid=True),
        nullable=False,
        unique=True,
    )

    umap_x: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    umap_y: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    umap_z: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category_technical_key: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categories.technical_key"),
        nullable=False,
    )

    filename: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    anomalie_isolation_forest: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    anomalie_lof: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    anomalie_lof_label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    anomalie_isolation_forest_label: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    nearest_neighbors: Mapped[dict[str, float]] = mapped_column(
        JSONB,
        nullable=False,
        server_default=text("'{}'::jsonb"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    category: Mapped[Category] = relationship(
        back_populates="data_overviews",
    )


class LabelProposal(Base):
    __tablename__ = "label_proposal"

    technical_key: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    file_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category_technical_key: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("categories.technical_key"),
        nullable=False,
    )

    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    category: Mapped[Category] = relationship(
        back_populates="label_proposals",
    )
