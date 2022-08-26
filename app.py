from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash
import datetime

from config import config, env_config

port = int(env_config['PORT'])

app = Flask(__name__)
app.config.from_object(config[env_config['ENV']])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)


class User(db.Model):
    __tablename__ = 'dbuser'

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Lokasi(db.Model):
    __tablename__ = 'dblokasi'

    id_lokasi = db.Column(db.Integer, primary_key=True)
    lokasi = db.Column(db.String(300), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)

    def __init__(self, lokasi, longitude, latitude):
        self.lokasi = lokasi
        self.longitude = longitude
        self.latitude = latitude

    def __repr__(self):
        return '<id {}>'.format(self.id_lokasi)


class Data(db.Model):
    __tablename__ = 'dbdata'

    id_data = db.Column(db.Integer, primary_key=True)
    id_lokasi = db.Column(db.Integer, db.ForeignKey(
        'dblokasi.id_lokasi'), nullable=False)
    pergeseran = db.Column(db.Integer, nullable=False)
    waktu = db.Column(db.DateTime, nullable=False)
    lokasi = db.relationship('Lokasi')

    def __init__(self, id_lokasi, pergeseran, waktu):
        self.id_lokasi = id_lokasi
        self.pergeseran = pergeseran
        self.waktu = waktu

    def __repr__(self):
        return '<id {}>'.format(self.id_lokasi)


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User


class LokasiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Lokasi


class DataSchema(ma.SQLAlchemyAutoSchema):
    lokasi = ma.Nested(LokasiSchema)

    class Meta:
        model = Data


def format_response(data, message="success"):
    return jsonify({"message": message, "data": data, })


@app.route('/user', methods=["GET", "POST"])
def user_get_and_create():
    if request.method == "GET":
        serializer = UserSchema(many=True)
        users = User.query.all()
        return format_response(serializer.dump(users))

    elif request.method == "POST":
        username = request.json.get('username', '')
        password = request.json.get('password', '')

        serializer = UserSchema()
        user = User(username, password)

        db.session.add(user)
        db.session.commit()

        return format_response(serializer.dump(user))


@app.route("/user/<user_id>", methods=["GET", "PUT", "DELETE"])
def user_get_update_delete_by_id(user_id):
    if request.method == "GET":
        user = User.query.get(user_id)
        serializer = UserSchema()

        return format_response(serializer.dump(user))

    elif request.method == "PUT":
        username = request.json.get('username', '')
        password = request.json.get('password', '')

        user = User.query.get(user_id)

        user.username = username
        user.password = generate_password_hash(password)

        serializer = UserSchema()

        db.session.add(user)
        db.session.commit()

        return format_response(serializer.dump(user))

    elif request.method == "DELETE":
        user = User.query.get(user_id)
        serializer = UserSchema()

        db.session.delete(user)
        db.session.commit()

        return format_response(serializer.dump(user))


@app.route('/lokasi', methods=["GET", "POST"])
def lokasi_get_and_create():
    if request.method == "GET":
        serializer = LokasiSchema(many=True)
        lokasi = Lokasi.query.all()
        return format_response(serializer.dump(lokasi))

    elif request.method == "POST":
        lokasi = request.json.get('lokasi', '')
        longitude = request.json.get('password', '')
        latitude = request.json.get('password', '')

        serializer = LokasiSchema()
        lokasi = User(lokasi, longitude, latitude)

        db.session.add(lokasi)
        db.session.commit()

        return format_response(serializer.dump(lokasi))


@app.route('/lokasi/<id_lokasi>', methods=["GET", "PUT", "'DELETE"])
def lokasi_get_update_delete_by_id(id_lokasi):
    if request.method == "GET":
        lokasi = Lokasi.query.get(id_lokasi)
        serializer = LokasiSchema()

        return format_response(serializer.dump(lokasi))

    elif request.method == "PUT":
        lokasi = request.json.get('lokasi', '')
        longitude = request.json.get('password', '')
        latitude = request.json.get('password', '')

        get_lokasi = Lokasi.query.get(id_lokasi)

        get_lokasi.lokasi = lokasi
        get_lokasi.longitude = longitude
        get_lokasi.latitude = latitude

        serializer = LokasiSchema()

        db.session.add(get_lokasi)
        db.session.commit()

        return format_response(serializer.dump(get_lokasi))

    elif request.method == "DELETE":
        lokasi = Lokasi.query.get(id_lokasi)
        serializer = LokasiSchema()

        db.session.delete(lokasi)
        db.session.commit()

        return format_response(serializer.dump(lokasi))


@app.route('/data', methods=["GET", "POST"])
def data_get_and_create():
    if request.method == "GET":
        serializer = DataSchema(many=True)
        data = Data.query.all()

        for i in data:
            print(i.__dict__['id_lokasi'])
        return format_response(serializer.dump(data))

    elif request.method == "POST":
        id_lokasi = request.json.get('id_lokasi', '')
        pergeseran = request.json.get('pergeseran', '')

        cur_time = datetime.datetime.now()

        serializer = DataSchema()
        data = Data(id_lokasi=id_lokasi, pergeseran=pergeseran, waktu=cur_time)

        db.session.add(data)
        db.session.commit()

        return format_response(serializer.dump(data))


@app.route('/data/<id_data>', methods=["GET", "PUT", "DELETE"])
def data_get_update_delete_by_id(id_data):
    if request.method == "GET":
        data = Data.query.get(id_data)
        serializer = DataSchema()

        return format_response(serializer.dump(data))

    elif request.method == "PUT":
        id_lokasi = request.json.get('id_lokasi', '')
        pergeseran = request.json.get('pergeseran', '')

        cur_time = datetime.datetime.now()

        serializer = DataSchema()
        data = Data.query.get(id_data)

        data.id_lokasi = id_lokasi
        data.pergeseran = pergeseran
        data.waktu = cur_time

        serializer = DataSchema()

        db.session.add(data)
        db.session.commit()

        return format_response(serializer.dump(data))

    elif request.method == "DELETE":
        data = Data.query.get(id_data)
        serializer = DataSchema()

        db.session.delete(data)
        db.session.commit()

        return "successfully delete"


if __name__ == '__main__':
    app.run(port=port)
