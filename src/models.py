from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import db


class Map(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    map_id: Mapped[str] = mapped_column(nullable=False)
    bucket_path: Mapped[str] = mapped_column(nullable=False)

    points: Mapped[List["Point"]] = relationship(back_populates="map_")


class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    map_id: Mapped[int] = mapped_column(ForeignKey("map.id"))
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    icon_path: Mapped[str] = mapped_column(nullable=True)

    map_: Mapped["Map"] = relationship(back_populates="points")
