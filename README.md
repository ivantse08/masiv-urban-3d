# 🏙️ Calgary Urban Building 3D Viewer

A web-based 3D visualization tool for exploring building data, including interactive filtering powered by a Large Language Model (LLM).

---

## 🚀 Live Demo

- **Frontend (React/Vercel)**: [https://masiv-urban-3d.vercel.app](https://masiv-urban-3d.vercel.app)
- **Backend (Flask/Render)**: [https://masiv-urban-3d.onrender.com](https://masiv-urban-3d.onrender.com)
 Note: Backend is API-only and does **not serve any visual content**—just JSON responses consumed by the frontend.
---

## 🧠 Features

- 3D buildings rendered centered around the University of Calgary from geospatial footprint and height data using React Three Fiber.
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

- The backend uses **Flask** to serve two main endpoints:
  - `GET /api/buildings`: Returns all building footprints within a fixed radius (centered in downtown Calgary), including building height and extra metadata.
  - `POST /api/query`: Accepts a natural language query, interprets it using a Hugging Face LLM, and returns a filtered list of matching buildings.

- Two **GeoJSON datasets from the City of Calgary** are fetched dynamically:
  - One dataset contains **building footprints** along with elevation info. This dataset took priority for rendering
  - The other contains **supplementary metadata**, such as:
    - Building code and description
    - Shape area and perimeter
    - Obscurity flag

- The datasets are merged using **GeoPandas** via a spatial join:
  - Footprints and metadata are matched using `sjoin` based on their geometry intersections.
  - Buildings without matching metadata are still retained with default values like `"Unknown"` or `-1`.
  - Due to possible mismatches of the building datasets, metadata about the building may not be extremely precise (i.e. 2 buildings exist as seperate in rendering but exist as one in metadata causing for some buildings to have same area/length when they're right next to each other even if they're different)

- NaN and missing values are handled safely to ensure the final JSON is valid and frontend-compatible.

- The backend is deployed using **Render**, with automatic deployment from GitHub on each push.

### 💻 Frontend (React + Vercel)

- The frontend is built using **React** with **React Three Fiber** for 3D rendering.
- It renders a 3D map of Calgary buildings by extruding their footprint polygons using:
  - `rooftop_elev_z` and `grd_elev_min_z` to calculate building height.
  - `coordinates` for the footprint geometry.

- **Technologies used**:
  - [`three.js`](https://threejs.org/) + [`@react-three/fiber`](https://docs.pmnd.rs/react-three-fiber): For interactive 3D visualization.
  - [`@react-three/drei`](https://github.com/pmndrs/drei): For camera controls and helpers like `OrbitControls`.
  - **React Hooks** (`useEffect`, `useState`) for fetching and rendering data.
  - **Vercel** for seamless frontend deployment from GitHub.

- **Key features**:
  - **Live 3D rendering** of building footprints based on real-world elevation data.
  - **Interactive popups** with metadata on click (e.g., height, stage, building code, area ).
  - **Natural Language Querying**: Users can type queries like `"show buildings taller than 30m"` and see filtered results.
  - **Error handling** for failed API calls or invalid responses (e.g., JSON decoding).

- **Data flow**:
  1. On load, the app fetches data from the Flask backend via `GET /api/buildings`.
  2. Buildings are rendered in 3D using their shape and height data.
  3. Users can enter natural language filters, which are sent via `POST /api/query` to the backend.
  4. The view updates in real-time based on the filtered result.

- Hosted on:  
  **[https://masiv-urban-3d.vercel.app](https://masiv-urban-3d.vercel.app)**

> ⚠️ **Note**: Not all building footprints had a matching metadata entry in the supplementary dataset due to slight differences in geometry or missing overlap.  
> To ensure completeness of the 3D scene, all valid building footprints are included.  
> If metadata was missing, default fallback values like `"Unknown"` or `-1` are used for those fields.  
> This means not every building has the exact same metadata structure as specified in the original datasets — this was a conscious trade-off to preserve spatial accuracy and visual continuity.
