import io
from unittest.mock import patch, MagicMock

from sqlalchemy.orm import Session

from database import engine
import models


# This file use fixtures from conftest.py


def test_hello_world(client):
    """
    Root path must return a hello world message.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"<p>Hello, World!</p>"


def test_get_maps(client):
    """
    Should be possible to get a list of created maps.
    """
    with patch("app.get_all_maps") as mocked_get_maps:
        mock_object1 = MagicMock()
        mock_object1.name = "Map 1"
        mock_object1.map_id = "map1.png"

        mock_object2 = MagicMock()
        mock_object2.name = "Map 2"
        mock_object2.map_id = "map2.png"

        mocked_get_maps.return_value = [mock_object1, mock_object2]

        response = client.get("/map")

        assert response.status_code == 200
        mocked_get_maps.assert_called_once()
        assert b"Map 1" in response.data
        assert b"Map 2" in response.data


def test_create_map(client):
    """
    Should be possible to create a new map.
    """
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
    """
    Should be possible add points to a pre existing map.
    """
    with Session(engine) as session:
        map_ = models.Map(
            name="map-test",
            map_id="c6d525d480a94e2987e10726713fb3ba",
            bucket_path="file-test.png",
        )
        session.add(map_)
        session.commit()
        map_id = map_.id

    fake_file = io.BytesIO(b"dummy data")
    point_data = {
        "mapId": map_id,
        "pointName": "point-test",
        "pointDescription": "description-test",
        "pointPositionX": 10,
        "pointPositionY": 10,
        "pointIcon": (fake_file, "fake_file.png"),
    }

    with patch("app.upload_file") as mock_upload_file:
        response = client.post(
            "/point", data=point_data, content_type="multipart/form-data"
        )

    assert response.status_code == 200
    mock_upload_file.assert_called_once()

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
