
from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory storage: student ID -> student details
students = {
    1: {"id": 1, "course": "CSE", "name": "Vinay"},
    2: {"id": 2, "course": "ECE", "name": "Hafeez"}
}

next_id = 3


@app.route("/")
def home():
    return "App is working", 200


# READ: Get all students
@app.route("/students", methods=["GET"])
def get_students():
    return jsonify(list(students.values())), 200


# CREATE: Add a student
@app.route("/students", methods=["POST"])
def add_student():
    global next_id

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    data["id"] = next_id
    students[next_id] = data
    next_id += 1

    return jsonify(data), 201


# READ: Get one student
@app.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(students[id]), 200


# UPDATE: Replace/update student fields
@app.route("/students/<int:id>", methods=["PUT"])
def update_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    students[id].update(data)
    students[id]["id"] = id

    return jsonify(students[id]), 200


# PARTIAL UPDATE: Change selected fields
@app.route("/students/<int:id>", methods=["PATCH"])
def patch_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json()
    if not isinstance(data, dict):
        return jsonify({"error": "JSON object required"}), 400

    students[id].update(data)
    students[id]["id"] = id

    return jsonify(students[id]), 200


# DELETE: Remove a student
@app.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):
    if id not in students:
        return jsonify({"error": "Student not found"}), 404

    del students[id]
    return jsonify({"message": "Student deleted"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
