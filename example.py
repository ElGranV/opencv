from modules.tracking import Tracker
from modules.analysis import detect_area, DEFAULT_NUMBER_OF_AREAS
from modules.arduino_io import write_arduino, write_read
import cv2


trk = Tracker("person")
trk.init(0, 120)

angle = 0
old_angle = 0
old_area = 0

i=0
while True:
    success, bbox = trk.update(True)
    if success:
        area = detect_area(trk.video, bbox)
        angle = int(((90*area)/DEFAULT_NUMBER_OF_AREAS))
        if angle != old_angle:
            print(area)
            print("arduino :", write_read(angle))
        old_angle = angle
            

    if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
         break
    i+=1
