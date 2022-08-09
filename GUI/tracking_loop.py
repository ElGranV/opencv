import threading
from modules.tracking import Tracker, TRACKING_VIEW_NAME
import cv2

def tracking_loop_function(config, callback):
    trk = Tracker(config["TRACKING_TYPE"])
    trk.init(config["VIDEO_PATH"], config["DETECTION_RATE"])
    callback()
    while True:
        success, bbox = trk.update(True)
        if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
            break
        if cv2.getWindowProperty(TRACKING_VIEW_NAME,cv2.WND_PROP_VISIBLE) < 1:        
            break
    

def tracking_loop(config, callback):
    process = threading.Thread(target=tracking_loop_function, args=(config, callback))
    process.start()
    

