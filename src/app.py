import os

from flask import Flask, request, render_template
from minio import Minio

from database import db
from models import Map


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
db.init_app(app)

# Create tables on database
with app.app_context():
    db.create_all()

# Init minio
minio_client = Minio(
    os.getenv("MINIO_ENDPOINT"),
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)
minio_bucket_name = "rpg"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/map", methods=["GET", "POST"])
def rpg_map():
    if request.method == "POST":
        map_name = request.form["mapName"]
        map_file = request.files["mapFile"]
        try:
            # Make the bucket if it doesn't exist.
            found = minio_client.bucket_exists(minio_bucket_name)
            if not found:
                minio_client.make_bucket(minio_bucket_name)
            # Upload file
            object_size = os.fstat(map_file.fileno()).st_size
            minio_client.put_object(
                minio_bucket_name,
                map_file.filename,
                map_file,
                object_size,
            )
        except Exception as error:
            return str(error)
        return "Map uploaded!"
    else:
        maps = minio_client.list_objects(minio_bucket_name)
        return render_template("list_maps.html", maps=maps)


@app.route("/create-map")
def create_map_form():
    return render_template("create_map.html")
