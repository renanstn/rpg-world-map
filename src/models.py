from sqlalchemy.orm import Mapped, mapped_column

from database import db


class Map(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    map_id: Mapped[str] = mapped_column(nullable=False)
    bucket_path: Mapped[str] = mapped_column(nullable=False)


class Point(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    icon_path: Mapped[str] = mapped_column(nullable=True)
