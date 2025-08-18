from flask import Blueprint, Response, request, jsonify
from db import create_overlay, get_overlays, update_overlay, delete_overlay
import cv2
import os
import logging
import bson
import urllib.parse
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Enable FFmpeg debug logging
os.environ['OPENCV_FFMPEG_DEBUG'] = '1'

routes = Blueprint('routes', __name__)

@routes.route('/hi')
def home():
    return "Hello, World!"

@routes.route('/video_feed')
def video_feed():
    source = request.args.get('url')
    if not source:
        logger.error("Missing source URL or file path")
        return jsonify({"error": "Missing source URL or file path"}), 400

    # Handle RTSP authentication
    parsed_url = urllib.parse.urlparse(source)
    if parsed_url.scheme == 'rtsp' and parsed_url.username and parsed_url.password:
        source = f"rtsp://{urllib.parse.quote(parsed_url.username)}:{urllib.parse.quote(parsed_url.password)}@{parsed_url.hostname}:{parsed_url.port or 554}{parsed_url.path}"
        if parsed_url.query:
            source += f"?{parsed_url.query}"

    if source.startswith(('rtsp://', 'http://', 'https://')):
        # Try opening stream with default FFmpeg settings, retrying for stability
        for attempt in range(3):
            logger.info(f"Attempting to open {source} (attempt {attempt + 1}/3)")
            cap = cv2.VideoCapture(source, cv2.CAP_FFMPEG)
            if cap.isOpened():
                success, _ = cap.read()
                if success:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to start
                    break
                else:
                    logger.warning(f"Failed to read initial frame from {source}")
                    cap.release()
            logger.warning(f"Failed to open {source} on attempt {attempt + 1}")
            time.sleep(2)  # Delay between retries
        else:
            logger.error(f"Failed to open stream: {source}. All attempts failed.")
            return jsonify({"error": f"Failed to open stream: {source}. Check URL, credentials, network, or firewall. FFmpeg logs may provide details."}), 404
    else:
        source = os.path.join(os.path.dirname(__file__), source)
        if not os.path.exists(source):
            logger.error(f"File not found: {source}")
            return jsonify({"error": f"File not found: {source}"}), 404
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            logger.error(f"Failed to open local file: {source}")
            return jsonify({"error": f"Failed to open file: {source}"}), 404

    def generate():
        try:
            while True:
                success, frame = cap.read()
                if not success:
                    logger.warning(f"Failed to read frame from {source}")
                    break
                ret, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                if not ret:
                    logger.warning(f"Failed to encode frame from {source}")
                    break
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except cv2.error as e:
            logger.error(f"OpenCV error for {source}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Stream error for {source}: {str(e)}")
            raise
        finally:
            logger.info(f"Releasing video capture for {source}")
            cap.release()

    try:
        logger.info(f"Starting MJPEG stream for {source}")
        return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except cv2.error as e:
        logger.error(f"OpenCV stream initialization error for {source}: {str(e)}")
        return jsonify({"error": f"OpenCV stream error: {str(e)}"}), 500
    except Exception as e:
        logger.error(f"Stream initialization error for {source}: {str(e)}")
        return jsonify({"error": f"Stream error: {str(e)}"}), 500

@routes.route('/overlays', methods=['GET'])
def get_overlays_route():
    try:
        data = get_overlays()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error fetching overlays: {str(e)}")
        return jsonify({"error": str(e)}), 500

@routes.route('/overlays', methods=['POST'])
def create_overlay_route():
    try:
        data = request.get_json()
        if not data or 'position' not in data or 'size' not in data:
            logger.error("Position and size are required")
            return jsonify({"error": "Position and size are required"}), 400
        overlay_id = create_overlay(data)
        logger.info(f"Created overlay with ID: {overlay_id}")
        return jsonify({"id": overlay_id}), 201
    except Exception as e:
        logger.error(f"Error creating overlay: {str(e)}")
        return jsonify({"error": str(e)}), 400

@routes.route('/overlays/<id>', methods=['PUT'])
def update_overlay_route(id):
    try:
        data = request.get_json()
        if update_overlay(id, data):
            logger.info(f"Updated overlay with ID: {id}")
            return jsonify({"message": "Updated"})
        logger.warning(f"Overlay not found: {id}")
        return jsonify({"error": "Not found"}), 404
    except bson.errors.InvalidId:
        logger.error(f"Invalid ID format: {id}")
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        logger.error(f"Error updating overlay: {str(e)}")
        return jsonify({"error": str(e)}), 400

@routes.route('/overlays/<id>', methods=['DELETE'])
def delete_overlay_route(id):
    try:
        if delete_overlay(id):
            logger.info(f"Deleted overlay with ID: {id}")
            return jsonify({"message": "Deleted"})
        logger.warning(f"Overlay not found: {id}")
        return jsonify({"error": "Not found"}), 404
    except bson.errors.InvalidId:
        logger.error(f"Invalid ID format: {id}")
        return jsonify({"error": "Invalid ID format"}), 400
    except Exception as e:
        logger.error(f"Error deleting overlay: {str(e)}")
        return jsonify({"error": str(e)}), 400