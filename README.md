<!-- PROJECT LOGO -->


<h1 align="center">AI-Enhanced Quality Inspection System</h1>

<p align="center">
  <b>A scalable backend for a cloud-based quality control web application that leverages AI and computer vision to detect manufacturing defects in real-time.</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.95+-green?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-brightgreen" alt="Status">
</p>

---

## 📑 Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Setup](#setup)
- [Usage](#usage)
- [API Overview](#api-overview)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features
- 📷 RESTful APIs for image uploads, inspection, and defect reports
- 🤖 PyTorch-based defect detection
- 🖼️ Image preprocessing with OpenCV/PIL
- 🔒 JWT-secured endpoints
- 🗄️ PostgreSQL for user and defect data
- ☁️ Azure deployment and monitoring

## 🛠️ Tech Stack
- **Python 3.10**
- **FastAPI**
- **PyTorch**
- **OpenCV, PIL**
- **PostgreSQL**
- **Azure (App Services, Blob Storage, Monitor)**
- **Docker**
- **JWT Authentication**

## 🚀 Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai_quality_inspection.git
   cd ai_quality_inspection
   ```
2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your settings.

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📦 Usage
- Access the API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)
- Upload images, inspect for defects, and generate reports via the API endpoints.

## 📚 API Overview
- `POST /upload` — Upload an image for inspection
- `POST /inspect` — Run AI-based defect detection
- `GET /reports` — Retrieve inspection reports
- `POST /auth/login` — Obtain JWT token

> For detailed API usage, see the [API documentation](http://localhost:8000/docs) after running the server.

## 🤝 Contributing
Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.

