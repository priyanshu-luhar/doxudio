from flask import Flask, request, send_file, jsonify
import sqlite3
import io
import os

app = Flask(__name__)
DB_NAME = "files.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY,
            filename TEXT,
            content BLOB,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    content = file.read()
    conn = sqlite3.connect(DB_NAME)
    conn.execute("INSERT INTO files (filename, content) VALUES (?, ?)", (file.filename, content))
    conn.commit()
    conn.close()
    return "Uploaded", 200

@app.route("/files", methods=["GET"])
def list_files():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, filename, uploaded_at FROM files")
    files = cur.fetchall()
    conn.close()
    return jsonify(files)

@app.route("/download/<int:file_id>", methods=["GET"])
def download(file_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT filename, content FROM files WHERE id=?", (file_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        filename, content = row
        return send_file(io.BytesIO(content), download_name=filename, as_attachment=True)
    return "File not found", 404

if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=True)
