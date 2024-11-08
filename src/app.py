import os
import uuid

from flask import Flask, request, render_template, jsonify

from database import db
from models import Map, Point
from bucket import (
    MINIO_BUCKET_NAME,
    minio_client,
    create_bucket_if_not_exist,
    upload_file,
    get_minio_path,
)
from utils import (
    create_map,
    get_all_maps,
    get_map_by_id,
    get_map_by_link,
    create_point,
    get_map_points,
)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Create tables on database
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/map", methods=["GET", "POST"])
def rpg_map():
    if request.method == "POST":
        map_name = request.form["mapName"]
        map_file = request.files["mapFile"]
        try:
            create_bucket_if_not_exist()
            upload_file(map_file)
            map_id = str(uuid.uuid4().hex)
            create_map(
                {
                    "name": map_name,
                    "map_id": map_id,
                    "bucket_path": map_file.filename,
                }
            )
        except Exception as error:
            # FIXME: better error handling
            raise Exception(str(error))
        return f"Map uploaded! ID: {map_id}"
    else:
        # maps = minio_client.list_objects(MINIO_BUCKET_NAME)
        maps = get_all_maps()
        return render_template("list_maps.html", maps=maps)


@app.route("/create-map")
def create_map_form():
    return render_template("create_map.html")


@app.route("/map/<map_id>")
def load_map(map_id):
    map_object = get_map_by_link(map_id)
    points_object = get_map_points(map_id)
    map_url = get_minio_path(map_object.bucket_path)
    points = []
    for point in points_object:
        points.append(
            {
                "id": point.id,
                "name": point.name,
                "description": point.description,
                "path": get_minio_path(point.icon_path),
                "x": point.position_x,
                "y": point.position_y,
            }
        )
    return render_template(
        "map.html",
        map_name=map_object.name,
        map_id=map_object.id,
        image_url=map_url,
        points=points,
    )


@app.route("/map/<map_id>/edit")
def edit_map(map_id):
    map_object = get_map_by_link(map_id)
    map_url = get_minio_path(map_object.bucket_path)
    return render_template(
        "edit_map.html",
        map_name=map_object.name,
        map_id=map_object.id,
        image_url=map_url,
    )


@app.route("/point", methods=["GET", "POST"])
def point():
    if request.method == "POST":
        name = request.form["pointName"]
        map_id = request.form["mapId"]
        description = request.form["pointDescription"]
        position_x = request.form["pointPositionX"]
        position_y = request.form["pointPositionY"]
        icon_file = request.files["pointIcon"]
        try:
            map_object = get_map_by_id(map_id)
            upload_file(icon_file)
            create_point(
                {
                    "name": name,
                    "map_id": map_object.id,
                    "description": description,
                    "icon_path": icon_file.filename,
                    "position_x": position_x,
                    "position_y": position_y,
                }
            )
        except Exception as error:
            # FIXME: better error handling
            raise Exception(str(error))
        return "Point created!"

    else:
        return "todo..."
