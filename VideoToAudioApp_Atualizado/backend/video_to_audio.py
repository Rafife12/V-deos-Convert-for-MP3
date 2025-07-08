from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
from moviepy.editor import VideoFileClip
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Configurações
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'audios'
DB_NAME = 'videotoaudio.db'

# Criação de diretórios
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Inicialização do app
app = Flask(__name__)
CORS(app)

# Função para criar o banco e a tabela se não existirem
def inicializar_banco():
    with sqlite3.connect(DB_NAME) as conexao:
        cursor = conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_video TEXT,
                nome_audio TEXT,
                data TEXT
            )
        ''')
        conexao.commit()

inicializar_banco()

@app.route("/upload", methods=["POST"])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"erro": "Arquivo de vídeo não enviado."}), 400

    video = request.files['video']
    if video.filename == '':
        return jsonify({"erro": "Nome do arquivo inválido."}), 400

    filename = secure_filename(video.filename)
    path_video = os.path.join(UPLOAD_FOLDER, filename)
    video.save(path_video)

    try:
        # Processa o vídeo e extrai o áudio
        clip = VideoFileClip(path_video)
        audio_filename = os.path.splitext(filename)[0] + ".mp3"
        path_audio = os.path.join(OUTPUT_FOLDER, audio_filename)
        clip.audio.write_audiofile(path_audio)
        clip.close()

        # Salva no banco
        with sqlite3.connect(DB_NAME) as conexao:
            cursor = conexao.cursor()
            sql = "INSERT INTO conversoes (nome_video, nome_audio, data) VALUES (?, ?, ?)"
            valores = (filename, audio_filename, datetime.now().isoformat())
            cursor.execute(sql, valores)
            conexao.commit()

        return jsonify({
            "mensagem": "Conversão realizada com sucesso!",
            "audio": audio_filename
        })

    except Exception as e:
        return jsonify({"erro": f"Erro ao converter o vídeo: {str(e)}"}), 500

@app.route("/conversoes", methods=["GET"])
def listar_conversoes():
    with sqlite3.connect(DB_NAME) as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM conversoes ORDER BY id DESC")
        resultados = [
            {"id": row[0], "nome_video": row[1], "nome_audio": row[2], "data": row[3]}
            for row in cursor.fetchall()
        ]
    return jsonify(resultados)

@app.route("/audios/<nome_audio>", methods=["GET"])
def baixar_audio(nome_audio):
    nome_audio = secure_filename(nome_audio)
    return send_from_directory(OUTPUT_FOLDER, nome_audio)

if __name__ == "__main__":
    app.run(debug=True)
