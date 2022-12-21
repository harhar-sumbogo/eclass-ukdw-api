from flask import Flask, jsonify, request
from eclass import Eclass
app = Flask(__name__)

list_session = {}


@app.route('/')
def hello_world():
    return "This API Call"


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json(force=True)
    nim = body["nim"]
    password = body["password"]
    if nim and password:
        session = Eclass(nim, password)

        try:
            session.login()
            list_session[nim] = session
            return {
                "success": True,
                "message": "success",
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    else:
        return {
            "success": False,
            "message": "Anda belum memberikan nim atau password pada body request"
        }


@app.route("/get_daftar_pengumuman/<nim>", methods=["GET"])
def daftar_pengumuman(nim):
    if nim in list_session:
        session = list_session[nim]

        return {
            "success": True,
            "results": session.get_daftar_pengumuman()
        }
    else:
        return {
            "success": False,
            "message": "Sesi anda habis atau belum login"
        }


@app.route("/get_detail_pengumuman/<nim>/<id>", methods=["GET"])
def detail_pengumuman(nim, id):
    if nim in list_session:
        session = list_session[nim]

        return {
            "success": True,
            "results": session.get_detail_pengumuman(id)
        }
    else:
        return {
            "success": False,
            "message": "Sesi anda habis atau belum login"
        }


app.run(host="localhost", port=5000)
