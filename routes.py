from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from models import User, Note

auth_bp = Blueprint("auth", __name__)
notes_bp = Blueprint("notes", __name__)

# --- AUTH ROUTES ---
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"id": user.id, "username": user.username}), 200

# --- NOTES ROUTES ---
@notes_bp.route("/", methods=["GET"])
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    notes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=5)
    return jsonify([{"id": n.id, "title": n.title, "content": n.content} for n in notes.items])

@notes_bp.route("/", methods=["POST"])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    note = Note(title=data["title"], content=data["content"], user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note created"}), 201

@notes_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_note(id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)
    db.session.commit()
    return jsonify({"message": "Note updated"}), 200

@notes_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(note)
    db.session.commit()
    return jsonify({"message": "Note deleted"}), 200