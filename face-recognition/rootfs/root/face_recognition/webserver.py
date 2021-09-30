"""Webserver to server Face recognition services."""

import base64
import sys
from http import HTTPStatus
from io import BytesIO
from os.path import exists

import face_recognition
import numpy as np
from flask import Flask, jsonify, request
from slugify import slugify

app = Flask(__name__)

@app.route("/recognize", methods=["POST"])
def recognize_face():
    """Identify faces in image."""
    if "image" not in request.json:
        return "'image' field is missing.", HTTPStatus.BAD_REQUEST
    
    image = face_recognition.load_image_file(BytesIO(base64.b64decode(request.json["image"])))
    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return jsonify(error="No faces recognized in image.")
    
    stored_faces_db = np.load("/config/face_recognition/faces_db.npz")
    stored_names = stored_faces_db.files
    if not stored_names:
        faces = {}
        i = 1
        for face_location in face_locations:
            faces[f"Unknown-{i}"] = face_location
            i = i + 1
        return jsonify(results=faces)

    stored_face_encodings = list(stored_faces_db.values())
    face_encodings = face_recognition.face_encodings(image, face_locations)
    faces_detected = []
    i = 1
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(
            stored_face_encodings, face_encoding
        )
        face_distances = face_recognition.face_distance(
            stored_face_encodings, face_encoding
        )
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = stored_names[best_match_index]
        else:
            name = f"Unknown-{i}"
            i = i + 1
        faces_detected.append(name)

    return jsonify(results=dict(zip(faces_detected, face_locations)))

@app.route("/faces", methods=["GET", "POST", "DELETE"])
def add_known_face():
    """Add new face to npy db file."""
    stored_faces_db = np.load("/config/face_recognition/faces_db.npz")

    stored_faces = {
        name: face_encoding for name, face_encoding in stored_faces_db.items()
    }

    response_code = HTTPStatus.OK
    
    if request.method == "POST":
        content = request.json
        if "name" not in content or "image" not in content:
            return jsonify(error="Body must include 'name' and 'image' keys."), HTTPStatus.BAD_REQUEST

        name = slugify(content["name"], separator='_')
        face_encoding = face_recognition.face_encodings(
            face_recognition.load_image_file(
                BytesIO(base64.b64decode(content["image"]))
            )
        )[0]
        stored_faces.update({name: face_encoding})
        response_code = HTTPStatus.CREATED

    if request.method == "DELETE":
        if "name" not in request.json:
            return jsonify(error="'name' field is missing."), HTTPStatus.BAD_REQUEST

        name = request.json["name"]
        if name == '*':
            stored_faces = {}
        elif name not in stored_faces:
            return jsonify(error="Face name not found."), HTTPStatus.NOT_FOUND
        else:
            stored_faces.pop(name)

    np.savez("/config/face_recognition/faces_db.npz", **stored_faces)
    response = list(stored_faces.keys())
    return jsonify(results=response), response_code


def Initialize():
    """Initialize Webserver."""
    if not exists("/config/face_recognition/faces_db.npz"):
        np.savez("/config/face_recognition/faces_db.npz")
    debug = False
    if len(sys.argv) > 1:
        debug= sys.argv[1] == "DEBUG" 
    app.run(host="0.0.0.0", port=5001, debug=debug)

if __name__ == "__main__":
    Initialize()
