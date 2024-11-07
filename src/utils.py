from typing import List, Optional

from sqlalchemy.orm import Session

from database import engine
from models import Map, Point


def create_map(data: dict) -> Map:
    with Session(engine) as session:
        map_ = Map(**data)
        session.add(map_)
        session.commit()
    return map_


def get_all_maps() -> List[Map]:
    with Session(engine) as session:
        maps = session.query(Map).all()
    return maps


def get_map_by_id(map_id: int) -> Optional[List[Map]]:
    with Session(engine) as session:
        map_ = session.query(Map).filter(Map.id == map_id).first()
    return map_


def get_map_by_link(map_link: str) -> Optional[Map]:
    with Session(engine) as session:
        map_ = session.query(Map).filter(Map.map_id == map_link).first()
    return map_


def get_map_points(map_id: int) -> Optional[List[Point]]:
    with Session(engine) as session:
        map_ = session.query(Map).filter(Map.map_id == map_id).first()
        points = session.query(Point).filter(Point.map_id == map_.id).all()
    return points


def create_point(data: dict) -> Point:
    with Session(engine) as session:
        point = Point(**data)
        session.add(point)
        session.commit()
    return point
