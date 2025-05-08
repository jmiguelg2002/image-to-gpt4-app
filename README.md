# 🧠 OpenAI Assistant App

A powerful and user-friendly assistant built with Streamlit that combines:

- 📝 Prompt input
- 🖼️ Image upload (Vision model support)
- 📄 File upload (PDF, DOCX, TXT, XLSX)
- 🎙️ Voice input with transcription (via Whisper)
- 🗣️ Spoken assistant replies (via TTS)

## 🚀 Features

| Feature        | Description |
|----------------|-------------|
| Text Prompt    | Input any question or command |
| File Upload    | Supports PDF, DOCX, TXT, and Excel (XLSX) |
| Image Upload   | Vision support using `gpt-4-turbo` |
| Voice Input    | Record voice → Whisper transcription |
| Audio Output   | TTS assistant replies with `tts-1` voice |
| Persistent Chat | Keeps conversation context in session |

## 📸 Screenshot

> *(Optional)* Add a screenshot of your deployed Streamlit app here.

## 🧰 Requirements

```bash
pip install -r requirements.txt
```

Also, create a secrets file at `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "sk-proj-..."
```

## 🛠 How to Run

```bash
streamlit run app_fixed.py
```

## 🌐 Live Demo

> Deployed on [Streamlit Cloud](https://your-deployment-url.streamlit.app)

---

Built with ❤️ using [Streamlit](https://streamlit.io), [OpenAI API](https://platform.openai.com), and Python.