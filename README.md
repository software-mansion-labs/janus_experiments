# Janus experiments

Both assume janus is runnning on localhost and http server is serving demos on port http://localhost:8000

## VideoRoom Loop

1. Open and start Video Room plugin demo (http://localhost:8000/videoroomtest.html)
2. Run `python videoroom_loop.py`
3. A new Remote Video should appear in the room being a reflection of first publisher in the room for ~10 seconds

## Video Room to Video Call bridge

1. Open and start Video Room plugin demo (http://localhost:8000/videoroomtest.html)
1. Open and start Video Call plugin demo (http://localhost:8000/videocalltest.html)
1. Register as `real` in the Video Call
1. Run `python vroom_to_vcall.py`
1. Within 30 seconds accept the call from `fake` in the browser
1. First publisher from Video Room should appear in the call for ~10 seconds
