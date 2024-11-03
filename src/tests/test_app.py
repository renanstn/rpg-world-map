from unittest.mock import patch, MagicMock

import pytest

from app import app


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
