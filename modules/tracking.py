import cv2
import time


TRACKING_TYPE = "CSRT"
TRACKING_VIEW_NAME = "Enov Tracking View"

class Tracker:
    #--------Static Attributes---------------
    CONFIG = {"FACE_CASCADE_SCALE_FACTOR":1.1,
    "FACE_CASCADE_MIN_NEIGHBORS":4 ,
    "HOG_WIN_STRIDE": (4,4),
    "HOG_SCALE":1.2,
    "DETECTION_RATE":120,
    "TRACKING_TYPE":"face",
    "VIDEO_PATH":0,
    }
    #----------------------------------------

    def __init__(self, type = "face"):
        """
        Cette classe doit permettre de simplifier le tracking d'une personne en train de parler devant une caméra, 
        ou en train de danser. Peut-être utilisé dans le cadre d'un système de suivi dynamique par caméra.
        Le fonctionnement allie détection automatique, soit par des alogrithmes de SVM (dans le cas d'une personne entièrement visible,
        on utilisee cv2.HOGDescriptor_getDefaultPeopleDetector) ou avec des modèles de reconnaissance faciale (dans le cas d'une personne proche
        de la caméra), et des méthodes d'Object Tracking.
        L'idée est de définir périodiquement une région ou se situe la personne suivie (par SVM ou face_cascade) puis de suivre cette
        région via un tracking CSRT, qui est beaucoup moins gourmand donc plus rapide, mais aussi moins précis.
        L'idée est que le tracking fonctionne en temps réel, et permette donc de piloter une action mécanique (comme un mouvement de servomoteur)
        en fonction de la position de la personne dans l'image.
        
        -----------------
        Attributes:
            box_tracker:
                Object Tracker de type CSRT
            frame_count: int
                compteur de frame
            detection_type: str
                type de detection (face ou person)
        
        -----------------
        ..todo::Ajouter l'évaluation de la distance
        """
        self.box_tracker = cv2.TrackerCSRT_create()
        self.frame_count = 0
        self.detection_type = type
        self.launch_detection = True
        
        if type == "face":
            self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        if type == "person":
            # initialisation du HOG:
            self.hog = cv2.HOGDescriptor()
            self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        
        self.config = Tracker.CONFIG
      


        

    
    def init(self, video_path = 0, detection_rate = 120):
        """
        Initialisation du tracker.
        -   Ouverture du flux vidéo. 
        -   Initialisation des valeurs
        
        Parameters
        ---------
        video_path: str
            Chemin vers le flux video. S'il vaut 0, cela ouvre la webcam. Peut lancer une exception en cas d'échec.
        detection_rate: int
            Nombre de frame au bout desquelles le script réenclenche une détection. Plus ce nombre est élevé plus le soin du tracking 
            est laissé au box tracking. Le box tracking étant moins gourmand que la detection faciale ou de pietons, c'est un équilibre à trouver
            en fonction du fps de la camera, pour ne pas trop ralentir le système. 
        """
        self.video = cv2.VideoCapture(video_path)
    # if video_path==0: time.sleep(500)
        if not self.video.isOpened():
            raise(RuntimeError("Erreur à l'ouverture du flux video"))
        if detection_rate > 0: self.detection_rate = detection_rate
        else: self.detection_rate = 50
        
    
    def update(self, show = False):
        """
        Met à jour la bounding box.

        Returns
        -------------
        List [success: Bool, bbox : tuple of coordinates for the bounding box]
        """
        
        #on récupère une frame du flux video
        ok, frame = self.video.read()
        
        if ok:
            #On redimensionne la taille de la frame et on la passe en noir et blanc pour accélérer la détection
            frame = cv2.resize(frame, (640, 480))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            
            #On incrémente le compteur de frame
            self.frame_count += 1
            #Si le compteur de frame est un multiple detection_rate on lance la détection
            if (self.frame_count-1) % self.detection_rate == 0: self.launch_detection = True
            
            if self.launch_detection:
                if show:
                    cv2.putText(frame, "Detection", (150,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

                boxes = self.detect(gray_frame)["boxes"]
                if len(boxes):
                    bbox = tuple(boxes[0])
                    success = True
                    #On initialise le "box_tracker" (object tracker) avec la box issue de la détection (face_cascade ou hog)
                    self.box_tracker.init(gray_frame, bbox)
                    self.launch_detection = False
                else:
                    success = False
                    bbox = None
                    
            else:
                success, bbox = self.box_tracker.update(frame)
                if not success: self.launch_detection = True
            
            self.frame_count += 1
            self.frame_count = self.frame_count % 100000
            
            if success: self.bbox = bbox
            #On peut afficher les images
            if show: self.show(frame, bbox, success)
            return [success, bbox]
        return [False, None]



    
    def detect(self, frame):
        """
        Parameters
        ------------
        frame: any
            frame/image provenant du flux vidéo (video.read())

        Returns
        -----------
        dict: dict
            {"boxes": liste de boxes où des individus ont été détectés}
        """
        if self.detection_type == "face":
            return{"boxes":self.face_cascade.detectMultiScale(frame, scaleFactor = self.config["FACE_CASCADE_SCALE_FACTOR"], 
            minNeighbors = self.config["FACE_CASCADE_MIN_NEIGHBORS"])}
        
        if self.detection_type == "person":
            boxes, weights = self.hog.detectMultiScale(frame, winStride = self.config["HOG_WIN_STRIDE"], 
            scale=self.config["HOG_SCALE"])
            return {"boxes": boxes, "weights": weights}
        
        return {"boxes":[]}
    
    def show(self, frame, bbox, success):
        # Draw bounding box
        if success:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, "Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        cv2.imshow(TRACKING_VIEW_NAME, frame)
    
    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()



