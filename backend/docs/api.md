API Documentation
Base URL
http://localhost:5000
Endpoints
1. GET /video_feed

Description: Streams MJPEG video from an RTSP URL, local file (e.g., movie.mp4), or HTTP video URL. Use in an <img> or <video> tag.
Query Parameters:
url (string, required): The RTSP URL (e.g., rtsp://192.168.x.x:8080/video), local file path (e.g., movie.mp4), or HTTP video URL.


Responses:
200 OK: Returns MJPEG stream (multipart/x-mixed-replace; boundary=frame).
400 Bad Request: If url is missing ({"error": "Missing source URL or file path"}).
404 Not Found: If the local file doesn’t exist ({"error": "File not found: <path>"}).


Example:<img src="http://localhost:5000/video_feed?url=rtsp://192.168.1.100:8080/video" />



2. POST /overlays

Description: Creates a new overlay and saves it to MongoDB.
Request Body (JSON):{
  "type": "text|logo",
  "content": "string",
  "position": { "x": number, "y": number },
  "size": { "w": number, "h": number }
}


Responses:
201 Created: Returns {"id": "<inserted_id>"}.
400 Bad Request: If position or size is missing ({"error": "Position and size are required"}).


Example:curl -X POST http://localhost:5000/overlays \
-H "Content-Type: application/json" \
-d '{"type":"text","content":"Hello","position":{"x":10,"y":20},"size":{"w":100,"h":50}}'



3. GET /overlays

Description: Retrieves all valid overlays from MongoDB.
Responses:
200 OK: Returns an array of overlays: [{id, type, content, position, size}, ...].
500 Internal Server Error: If database access fails ({"error": "<error message>"}).


Example Response:[
  {
    "id": "68a2c77326f160138155a17b",
    "type": "text",
    "content": "Hello",
    "position": { "x": 10, "y": 20 },
    "size": { "w": 100, "h": 50 }
  }
]


Example:curl http://localhost:5000/overlays



4. PUT /overlays/

Description: Updates an existing overlay by ID.
Path Parameters:
id (string): MongoDB ObjectId of the overlay.


Request Body (JSON): Partial or full overlay data (e.g., { "position": { "x": 15, "y": 25 } }).
Responses:
200 OK: If updated ({"message": "Updated"}).
400 Bad Request: If ID is invalid ({"error": "<error message>"}).
404 Not Found: If overlay doesn’t exist ({"error": "Not found"}).


Example:curl -X PUT http://localhost:5000/overlays/68a2c77326f160138155a17b \
-H "Content-Type: application/json" \
-d '{"position":{"x":15,"y":25}}'



5. DELETE /overlays/

Description: Deletes an overlay by ID.
Path Parameters:
id (string): MongoDB ObjectId of the overlay.


Responses:
200 OK: If deleted ({"message": "Deleted"}).
400 Bad Request: If ID is invalid ({"error": "<error message>"}).
404 Not Found: If overlay doesn’t exist ({"error": "Not found"}).


Example:curl -X DELETE http://localhost:5000/overlays/68a2c77326f160138155a17b \
-H "Content-Type: application/json"



Notes

All endpoints support CORS for http://localhost:3000 with methods GET, POST, PUT, DELETE, OPTIONS.
The /video_feed endpoint uses MJPEG, which doesn’t support audio. Use direct MP4 URLs for audio-enabled streams.
