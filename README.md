# 🎵 Conversor de Vídeo para MP3

Este projeto é uma aplicação web simples feita com Flask e HTML/CSS que permite converter vídeos em arquivos de áudio (formato MP3). Ele utiliza a biblioteca `moviepy` para extrair o áudio do vídeo enviado pelo usuário. Os dados das conversões são armazenados em um banco de dados (SQLite ou SQL Server).

---

## 📂 Funcionalidades

- Upload de vídeos diretamente do navegador.
- Conversão automática de vídeo para áudio (MP3).
- Download do arquivo convertido.
- Histórico de conversões armazenado no banco de dados.
- Interface moderna e responsiva com HTML + CSS puro.
- Backend configurável com SQLite ou SQL Server.

---

## 🚀 Tecnologias utilizadas

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** Python (Flask)
- **Banco de dados:** SQLite (padrão) ou SQL Server (opcional)
- **Bibliotecas Python:**
  - `flask`
  - `flask_cors`
  - `moviepy`
  - `werkzeug`
  - `pyodbc` (opcional, para SQL Server)

---

## 📁 Estrutura do Projeto

```
videotoaudio/
│
├── index.html                 # Interface web do usuário
├── video_to_audio_sqlite.py   # Backend com SQLite
├── create_database.sql        # Script SQL para criar banco no SQL Server
├── videotoaudio_sqlserver.zip # Pacote completo com todos os arquivos
└── README.md                  # Este arquivo
```

---

## 💻 Como executar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/videotoaudio.git
cd videotoaudio
```

### 2. Instale os pacotes necessários

```bash
pip install flask flask-cors moviepy
```

> 💡 Para uso com SQL Server, também instale:
> ```bash
> pip install pyodbc
> ```

### 3. Execute o backend

```bash
python video_to_audio_sqlite.py
```

> O servidor estará disponível em: [http://localhost:5000](http://localhost:5000)

### 4. Abra o frontend

Basta abrir o arquivo `index.html` no seu navegador.

---

## 🔗 Endpoints da API

- `POST /upload` – Envia o vídeo e retorna o link do áudio.
- `GET /conversoes` – Lista todas as conversões feitas.
- `GET /audios/<nome>` – Baixa o áudio convertido.

---

## 🗄️ Usando com SQL Server

- Execute o arquivo `create_database.sql` no SQL Server Management Studio.
- Adapte o backend usando `pyodbc` (posso te ajudar com isso).
- Configure string de conexão no seu `video_to_audio.py`.

---

## 📜 Licença

Este projeto é livre para uso educacional, pessoal e não-comercial.
