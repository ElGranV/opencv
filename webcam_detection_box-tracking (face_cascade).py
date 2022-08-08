import time
import cv2
import sys
import modules.move as move

OUTPUT_VID = False

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')


tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
tracker_type = tracker_types[7]

if int(minor_ver) < 3:
    tracker = cv2.Tracker_create(tracker_type)
else:
    if tracker_type == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    elif tracker_type == 'MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_type == 'KCF':
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == 'TLD':
        tracker = cv2.TrackerTLD_create()
    elif tracker_type == 'MEDIANFLOW':
        tracker = cv2.TrackerMedianFlow_create()
    elif tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
    elif tracker_type == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == "CSRT":
        tracker = cv2.TrackerCSRT_create()
# Read video
video = cv2.VideoCapture(0)
#video = cv2.VideoCapture(0) # for using CAM

# Exit if video not opened.
if not video.isOpened():
  print("Could not open video")
  sys.exit()

# Read first frame.
ok, frame = video.read()
if not ok:
  print ('Cannot read video file')
  sys.exit()

# Define an initial bounding box
bbox = (287, 23, 86, 320)

# Uncomment the line below to select a different bounding box
#bbox = cv2.selectROI(frame, False)

#on peut stocker le résultat
if OUTPUT_VID:
    out = cv2.VideoWriter(
    'DETECTION.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    
    40.,
    (640,480))

launch_detection = True
rounds = 0
orientation = 0

while True:
    rounds+=1
    rounds = rounds%50
    # Read a new frame
    ok, frame = video.read()
    if not ok:
         break
    
    if launch_detection:
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        boxes = face_cascade.detectMultiScale(gray, 1.1, 4 )
        if len(boxes):
            # print("first boxes", boxes)
            bbox = tuple(boxes[0])
            print("Direction ",["NEUTRAL", "LEFT", "RIGHT"][move.detect_direction(video, bbox)])

            ok = tracker.init(frame, bbox)
            launch_detection = False


     
    else:
        # Update tracker
        ok, bbox = tracker.update(frame)
        
        

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
    
    
    #display images :
    cv2.imshow("Tracking", frame)
    if  OUTPUT_VID: 
        frame = cv2.resize(frame, (640, 480))
        out.write(frame.astype('uint8'))
    
    # Display result
    if rounds==0: launch_detection = True

    if rounds%5==0:
        orientation = move.send_move_message(video, bbox, orientation)

     # Exit if ESC pressed
    if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
         break


video.release()
cv2.destroyAllWindows()