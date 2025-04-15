# 🏙️ Masiv Urban 3D Viewer

A web-based 3D visualization tool for exploring building data, including interactive filtering powered by a Large Language Model (LLM).

---

## 🚀 Live Demo

- **Frontend (React/Vercel)**: [https://masiv-urban-3d.vercel.app](https://masiv-urban-3d.vercel.app)
- **Backend (Flask/Render)**: [https://masiv-urban-3d.onrender.com](https://masiv-urban-3d.onrender.com)

---

## 🧠 Features

- 3D buildings rendered from geospatial footprint and height data using React Three Fiber.
- Query buildings using natural language powered by Hugging Face LLM.
- Filtered results update in real-time.
- Popup info on building click.
- Deployed frontend + backend using Vercel and Render.

---

## 🛠️ Technologies

- **Frontend**: React, Three.js, React Three Fiber, Vercel
- **Backend**: Flask, Hugging Face API, Render
- **3D Rendering**: Extruded building footprints based on rooftop elevation and ground elevation

---

## 🧑‍💻 Setup Instructions

### 📦 Backend (Flask + Render)

#### 1. Clone & install dependencies:
```bash
git clone https://github.com/ivantse08/masiv-urban-3d
cd backend
pip install -r requirements.txt
