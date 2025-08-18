User Guide: Livestream App
Overview
This app allows users to stream video from RTSP URLs, local MP4 files, or HTTP video URLs, with the ability to add, position, resize, and manage custom overlays (text or logos) on top of the stream. Overlays are saved to a MongoDB database via a RESTful API.
Setup
Prerequisites

Python 3.8+: For the backend.
Node.js 16+: For the frontend.
MongoDB: Running locally on mongodb://localhost:27017.
FFmpeg: Optional, for RTSP stream compatibility (ensure it’s in your system PATH).

Backend Setup

Navigate to the backend directory:cd backend


Install Python dependencies:pip install flask flask-cors pymongo opencv-python


Ensure MongoDB is running:mongosh


Run the backend:python app.py


The server runs on http://localhost:5000.
Ensure app.py, db.py, and routes.py are in the backend directory.



Frontend Setup

Navigate to the frontend directory:cd frontend


Install Node.js dependencies:npm install axios react-draggable@4.4.6 @testing-library/user-event@latest


Run the frontend:npm start


The app runs on http://localhost:3000.



Usage
Accessing the App

Open http://localhost:3000 in a web browser.

Playing a Livestream

Enter a Source URL:
In the input field, enter an RTSP URL (e.g., rtsp://192.168.1.100:8080/video from an IP camera), a local file path (e.g., movie.mp4), or an HTTP video URL (e.g., http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4).
Local files must be placed in the backend directory for the server to access them.


Play/Pause:
Click the "Play" button (▶️) to start streaming.
Click "Pause" (⏸) to pause the stream. The video player remains visible.


Volume Control:
For MP4 files, use the volume slider to adjust audio (0 to 100%).
For RTSP or MJPEG streams, the volume slider is disabled (no audio support).



Managing Overlays

Add an Overlay:
Select the overlay type (text or logo) from the dropdown.
Enter content:
For text, enter the text to display (e.g., "Live Stream").
For logo, enter an image URL (e.g., https://example.com/logo.png).


Click "Add Overlay" to save it to MongoDB.


Position and Resize:
Overlays appear on the video. Drag to reposition (updates position in MongoDB).
Resize by dragging the bottom-right corner (updates size in MongoDB).


View Saved Overlays:
The "Saved Overlays" list shows all overlays with their type, content, position, and size.


Delete an Overlay:
Click "Delete" next to an overlay in the list to remove it from MongoDB.



Example Workflow

Open http://localhost:3000.
Enter rtsp://192.168.1.100:8080/video or movie.mp4.
Click "Play" to start the stream.
Select "text" in the overlay dropdown, enter "Live Now", and click "Add Overlay".
Drag the overlay to a new position and resize it.
Delete the overlay from the list.

Notes

Audio Limitation: RTSP and MJPEG streams (via /video_feed) don’t support audio due to MJPEG’s image-based format. Volume control is available only for direct MP4 URLs (e.g., HTTP-hosted MP4 files).
Browser Autoplay: Some browsers block autoplay for videos with audio. If the video doesn’t start, click "Play" manually.
MongoDB: Overlays are stored in the claimss.overlays collection. Use mongosh to inspect:use claimss
db.overlays.find().pretty()


React Compatibility: Uses react-draggable@4.4.6 with nodeRef for React 19 compatibility.
Backend Structure: Refactored into app.py (app setup), db.py (MongoDB operations), and routes.py (routes) for modularity.
CORS: Configured to allow requests from http://localhost:3000.

Troubleshooting

Stream Fails: Ensure the RTSP URL is accessible or the file exists in the backend directory. Check backend logs (python app.py) for errors.
Overlay Issues: Verify MongoDB is running and the claimss.overlays collection is accessible. Clear invalid data:db.overlays.deleteMany({ position: { $exists: false } })


CORS Errors: Check the browser console (F12) for CORS issues. Ensure flask-cors is installed and configured in app.py.
Autoplay Blocked: If the MP4 video doesn’t play, click "Play" manually due to browser policies.
