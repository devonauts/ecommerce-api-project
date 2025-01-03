from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from models import db
from models.file import File
from schemas.file_schema import file_schema, files_schema

files_bp = Blueprint('files', __name__)

@files_bp.route("/", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(request.app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    new_file = File(filename=filename, file_path=file_path)
    db.session.add(new_file)
    db.session.commit()

    return file_schema.jsonify(new_file), 201

@files_bp.route("/", methods=["GET"])
def get_files():
    files = File.query.all()
    return files_schema.jsonify(files)

@files_bp.route("/<int:file_id>", methods=["GET"])
def download_file(file_id):
    file = File.query.get_or_404(file_id)
    return send_from_directory(request.app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@files_bp.route("/<int:file_id>", methods=["DELETE"])
def delete_file(file_id):
    file = File.query.get_or_404(file_id)
    os.remove(file.file_path)
    db.session.delete(file)
    db.session.commit()
    return jsonify({"message": "File deleted successfully"})
