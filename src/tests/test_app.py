import io
from unittest.mock import patch, MagicMock

import pytest
from sqlalchemy.orm import Session

from app import app, engine
import models


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"<p>Hello, World!</p>"


def test_get_maps(client):
    with patch("app.minio_client.list_objects") as mock_list_objects:
        mock_object1 = MagicMock()
        mock_object1.object_name = "map1.png"
        mock_object2 = MagicMock()
        mock_object2.object_name = "map2.png"

        mock_list_objects.return_value = [mock_object1, mock_object2]

        response = client.get("/map")

        assert response.status_code == 200
        assert b"map1.png" in response.data
        assert b"map2.png" in response.data


def test_create_map(client):
    data = {"mapName": "test map"}
    fake_file = io.BytesIO(b"dummy data")
    fake_file.name = "fake_file.png"
    data["mapFile"] = (fake_file, "fake_file.png")

    with patch("app.create_bucket_if_not_exist") as mock_create_bucket, patch(
        "app.upload_file"
    ) as mock_upload_file:
        response = client.post(
            "/map",
            data=data,
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        mock_create_bucket.assert_called_once()
        mock_upload_file.assert_called_once()


def test_add_point_to_map(client):
    map_id = "c6d525d480a94e2987e10726713fb3ba"
    with Session(engine) as session:
        map_ = models.Map(
            name="map-test",
            map_id=map_id,
            bucket_path="file-test.png",
        )
        session.add(map_)
        session.commit()

    fake_file = io.BytesIO(b"dummy data")
    point_data = {
        "mapId": map_id,
        "pointName": "point-test",
        "pointDescription": "description-test",
        "pointPositionX": 10,
        "pointPositionY": 10,
        "pointIcon": (fake_file, "fake_file.png"),
    }
    response = client.post(
        "/point", data=point_data, content_type="multipart/form-data"
    )

    assert response.status_code == 200

    with Session(engine) as session:
        point_stored: models.Point = (
            session.query(models.Point)
            .filter(models.Point.name == "point-test")
            .first()
        )

    assert point_stored is not None
    assert point_stored.name == "point-test"
    assert point_stored.description == "description-test"
    assert point_stored.icon_path == "fake_file.png"
