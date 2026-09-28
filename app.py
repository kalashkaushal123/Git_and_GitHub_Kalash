from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os

load_dotenv()

app = Flask(__name__)

#Mongo Atlasconnection
MONGO_URL = os.getenv("MONGO_URL")


client = MongoClient(MONGO_URL)
db = client["flask_mongodb_db"]
collection = db["users"]


#Task1 : JSON api route 
@app.route("/api")
def api():
    with open("data.json",'r') as file:
        data = json.load(file)

    return jsonify(data)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        try:
            name = request.form['name']
            email = request.form['email']
            course = request.form['course']
            data = {
                "name": name,
                "email": email,
                "course": course
            }
            collection.insert_one(data)

            return redirect(url_for("success"))
        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')


#success page
@app.route("/success")
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)