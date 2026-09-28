from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import os


app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URL"))

db = client["todo_database"]
todos = db["todos"]


@app.route("/")
def home():
    return render_template("todo.html")

@app.route("/submittodoitem", methods=["POST"])
def submit_todo_item():
    data = request.get_json()

    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({
            "error" : "itemName and itemDescription are required"
        }),400

    todo = {
        "itemName" : item_name,
        'itemDescription' : item_description
    }
    result = todos.insert_one(todo)

    return jsonify({
        "message" : "Todo item saved successfully",
        "id" : str(result.inserted_id)
    }),201


if __name__ == "__main__":
    app.run(debug=True)


