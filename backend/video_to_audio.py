
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from moviepy.editor import VideoFileClip
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# Inicializa Firebase
cred = credentials.Certificate("projav3-16d41-firebase-adminsdk-fbsvc-b6c6255875.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'audios'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"erro": "Arquivo de vídeo não enviado"}), 400

    video = request.files['video']
    filename = video.filename
    path_video = os.path.join(UPLOAD_FOLDER, filename)
    video.save(path_video)

    try:
        clip = VideoFileClip(path_video)
        audio_filename = filename.rsplit('.', 1)[0] + ".mp3"
        path_audio = os.path.join(OUTPUT_FOLDER, audio_filename)
        clip.audio.write_audiofile(path_audio)

        # Salva no Firebase
        dados = {
            "nome_video": filename,
            "nome_audio": audio_filename,
            "data": datetime.now().isoformat()
        }
        db.collection("conversoes").add(dados)

        return jsonify({
            "mensagem": "Conversão realizada com sucesso!",
            "audio": audio_filename
        }), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

@app.route("/conversoes", methods=["GET"])
def listar_conversoes():
    docs = db.collection("conversoes").stream()
    resultado = []
    for doc in docs:
        dados = doc.to_dict()
        dados["id"] = doc.id
        resultado.append(dados)
    return jsonify(resultado)

@app.route("/audios/<nome_audio>", methods=["GET"])
def baixar_audio(nome_audio):
    return send_from_directory(OUTPUT_FOLDER, nome_audio)

if __name__ == "__main__":
    app.run(debug=True)
