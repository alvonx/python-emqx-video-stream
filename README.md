# python-emqx-video-stream


## refer to this link to setup emqx
- https://github.com/alvonx/emqx-python

## publish-video.py
- fetch frames from the first camera
- convert the frame to bytes
- start sending the frame to emqx broker

## subscribe-video.py
- get the new message
- extract the bytes
- convert to image
- display
