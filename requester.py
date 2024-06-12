import cv2
from pathlib import Path
import requests
import numpy
url = "http://10.0.0.164:8000/send_frame"

def stream_frame(frame: numpy.ndarray):
    height, width, _ = frame.shape
    new_h = int (height / 2)
    new_w = int (width / 2)
    frame = cv2.resize(frame, (new_w, new_h))
    _, jpeg = cv2.imencode('.jpg', frame)
    frame_bytes = jpeg.tobytes()
    response = requests.post(url, data=frame_bytes, headers={'Content-Type': 'application/octet-stream'})
    print(response.json())

file_path = Path("2024-06-10T12-45-00.mp4")
cap = cv2.VideoCapture(file_path, cv2.CAP_FFMPEG)
#cap.set(cv2.CAP_PROP_POS_MSEC, 0)
        
while cap.isOpened():
    success, frame = cap.read()
    if success:
        print("S")
        stream_frame(frame)

        if cv2.waitKey(100) & 0xFF == ord('q'): 
          break
    else:
        break
cap.release()
cv2.destroyAllWindows()
      