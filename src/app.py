import os
import uuid

from flask import Flask, request, render_template
from sqlalchemy.orm import Session

from database import db, engine
from models import Map, Point
from bucket import (
    MINIO_BUCKET_NAME,
    minio_client,
    create_bucket_if_not_exist,
    upload_file,
    get_minio_path,
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
            with Session(engine) as session:
                map_ = Map(
                    name=map_name,
                    map_id=map_id,
                    bucket_path=map_file.filename,
                )
                session.add(map_)
                session.commit()
        except Exception as error:
            return str(error)
        return f"Map uploaded! ID: {map_id}"
    else:
        maps = minio_client.list_objects(MINIO_BUCKET_NAME)
        return render_template("list_maps.html", maps=maps)


@app.route("/create-map")
def create_map_form():
    return render_template("create_map.html")


@app.route("/map/<map_id>")
def load_map(map_id):
    with Session(engine) as session:
        map_object = session.query(Map).filter(Map.map_id == map_id).first()
    map_url = get_minio_path(map_object.bucket_path)
    return render_template(
        "map.html", map_name=map_object.name, image_url=map_url
    )


@app.route("/map/<map_id>/edit")
def update_map(map_id):
    with Session(engine) as session:
        map_object = session.query(Map).filter(Map.map_id == map_id).first()
    map_url = get_minio_path(map_object.bucket_path)
    return render_template(
        "edit_map.html", map_name=map_object.name, image_url=map_url
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
            with Session(engine) as session:
                map_object = (
                    session.query(Map).filter(Map.map_id == map_id).first()
                )
                if not map_object:
                    raise Exception(f"Map ID: '{map_id}' no found.")
                upload_file(icon_file)
                point = Point(
                    name=name,
                    map_id=map_object.id,
                    description=description,
                    icon_path=icon_file.filename,
                    position_x=position_x,
                    position_y=position_y,
                )
                session.add(point)
                session.commit()
        except Exception as error:
            return str(error)
        return "Point created!"

    else:
        return "todo..."
