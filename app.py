import os 
from bson.objectid import (ObjectId, InvalidId)
from flask import (
    Flask, jsonify, request)
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def get_route():
    return jsonify({"Message": "cats API root"})


@app.route("/cats", methods=["GET", "POST"])
def get_all_cats():
    cats = mongo.db.cats.find()
    cats = [{**cat, "_id": str(cat["_id"])} for cat in cats]
    if len(cats) == 0:
        return "", 204
    return jsonify(cats), 200


@app.route("/cats/<string:_id>")
def get_cat_by_id(_id):
    try:
        cat = mongo.db.cats.find_one({"_id": ObjectId(_id)})
        if not cat:
            raise FileNotFoundError("Cat not found")
        cat["_id"] = str(cat["_id"])
        return jsonify(cat), 200
    except (ValueError, NameError, TypeError) as err:
        return jsonify({"error": f"{err}"}), 400
    except FileNotFoundError as err:
        return jsonify({"error": f"{err}"}), 404
    except Exception as err:
        return jsonify({"error": "Internal server error"}), 500



class FileNotFoundError(Exception):
    pass