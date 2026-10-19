# StegoCraft – Intelligent Web-Based Multimedia Steganography System

> A Django-based web application for securely hiding secret messages inside **images**, **audio**, and **video** files using **LSB steganography** + **AES-256 encryption**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python) ![Django](https://img.shields.io/badge/Django-4.2-green?logo=django) ![AES](https://img.shields.io/badge/Encryption-AES--256-purple?logo=shield) ![LSB](https://img.shields.io/badge/Algorithm-LSB%20Steganography-orange)

---

## ✨ Features

- 🔐 **AES-256 encryption** — messages are encrypted before hiding
- 🖼️ **Image steganography** — hide messages in PNG/JPEG files
- 🎵 **Audio steganography** — hide messages in WAV files
- 🎬 **Video steganography** — hide messages in AVI files
- 📁 **Drag & Drop** file upload with live preview
- 🌙 **Dark / Light mode** toggle
- 📱 **Mobile responsive** design
- 🛡️ **File validation** with clear error messages
- 🔑 **Key-based decoding** — only the key holder can decode

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/StegoCraft.git
cd StegoCraft

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python manage.py runserver
```

### Open in browser
```
http://127.0.0.1:8000/
```

---

## 🛠️ How It Works

```
Your Message
    │
    ▼
AES-256 Encryption (random key)
    │
    ▼
LSB Embedding (into image/audio/video)
    │
    ▼
Download ZIP (encoded file + key.txt)
```

To decode:
```
Encoded File + Key
    │
    ▼
LSB Extraction
    │
    ▼
AES-256 Decryption
    │
    ▼
Original Message ✅
```

---

## 📁 Project Structure

```
StegoCraft/
├── algorithms/
│   ├── crypto_utils.py     # AES-256 encrypt/decrypt
│   ├── encode.py           # Audio LSB steganography
│   ├── encode_img.py       # Image LSB steganography
│   └── encode_video.py     # Video LSB steganography
├── StegoCraft/
│   ├── settings.py         # Django settings (uses .env)
│   ├── urls.py             # URL routing
│   └── views.py            # Request handlers
├── templates/              # HTML templates
├── .env                    # Environment variables (not committed)
├── .gitignore
├── manage.py
└── requirements.txt
```

---

## 🔒 Security Notes

- The `SECRET_KEY` is loaded from `.env` — never commit `.env` to GitHub
- AES-256-CBC with random IV is used for each encoding operation
- The decode key is included in the downloaded ZIP — store it safely

---

## 📜 License
MIT License — feel free to use and modify.
