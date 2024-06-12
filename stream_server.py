from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
import io

app = FastAPI()

# Global variable to store the received frame
stored_frame = cv2.imread("no_data.jpg")


@app.post("/send_frame")
async def send_frame(request: Request):
    global stored_frame
    # Read the body of the request
    body = await request.body()
    # Decode the image from the received bytes
    nparr = np.frombuffer(body, np.uint8)
    stored_frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return {"status": "frame received"}

@app.get("/get_video")
async def get_video():
    global stored_frame
    if stored_frame is None:
        return Response(content="No frame available", media_type="text/plain", status_code=404)

    # Convert the frame to a JPEG image
    _, jpeg = cv2.imencode('.jpg', stored_frame)
    frame_bytes = io.BytesIO(jpeg.tobytes())

    # Function to generate the streaming response
    async def frame_generator():
        while True:
            # Re-encode the stored frame to simulate streaming
            _, jpeg = cv2.imencode('.jpg', stored_frame)
            frame_bytes = io.BytesIO(jpeg.tobytes())
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes.read() + b'\r\n')

    return StreamingResponse(frame_generator(), media_type="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
