Livestream App

Overview
This is a livestream application built with a React frontend and Flask backend. It supports streaming from RTSP URLs, local MP4 files, or HTTP video URLs, with draggable and resizable overlays (text or logos) managed via a MongoDB database. The app includes play/pause controls, volume adjustment (for MP4 files), and a RESTful API for overlay CRUD operations.
Project Structure

livestream-app/
├── backend/
│   ├── docs/
│   │   └── api.md        # API documentation
│   ├── app.py            # Flask app setup
│   ├── db.py             # MongoDB operations
│   ├── routes.py         # Route handlers
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   ├── VideoStream.jsx
│   │   ├── VideoStream.css
│   ├── package.json
├── docs/
│   └── user.md           # User documentation
├── README.md

Setup

Prerequisites:

Python 3.8+
Node.js 16+
MongoDB (running on mongodb://localhost:27017)
FFmpeg (optional, for RTSP streams)


Backend:
cd backend
pip install flask flask-cors pymongo opencv-python
python app.py


Frontend:
cd frontend
npm install axios react-draggable@4.4.6 @testing-library/user-event@latest
npm start


MongoDB:

Ensure MongoDB is running (mongosh).
Overlays are stored in the claimss.overlays collection.



Running the App

Open http://localhost:3000.
Enter an RTSP URL (e.g., rtsp://192.168.1.100:8080/video), local file (movie.mp4), or HTTP MP4 URL.
Use play/pause, volume (MP4 only), and overlay management features.

Documentation

API: backend/docs/api.md details CRUD endpoints (/video_feed, /overlays).
User: docs/user.md explains setup and usage.

Notes

MJPEG streams (RTSP, /video_feed) don’t support audio; volume control is for MP4 only.
Uses react-draggable@4.4.6 for React 19 compatibility.
Backend is modular (app.py, db.py, routes.py).
