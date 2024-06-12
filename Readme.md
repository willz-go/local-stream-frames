# Stream frames from headless opencv

### Description
This method provides a way to stream any matLike frames from a headless envorionment
It uses a POST endpoint to receive its frame payload and a GET endpoint to view the last frame sent

- Launch StreamServer
- Send Post Request to /send_frame endpoint
- Remotely observes the frame throught /get_video stream endpoint on a webbrowser that has access to the server
