from flask import Flask, jsonify, request
from pymongo import MongoClient
import os


app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URL"))

db = client["todo_database"]
collection = db["todos"]


#Task1 : JSON api route 
@app.route("/submittodoitem", method=["POST"])
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