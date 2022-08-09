import tkinter as tk
# import filedialog module
from tkinter import filedialog
from turtle import back
from idlelib.tooltip import Hovertip
import os

from GUI.tracking_loop import tracking_loop
from modules.tracking import Tracker


class MainWindow(tk.Frame):
    def __init__(self, parent):
        super(MainWindow, self).__init__(parent)
        # self.columnconfigure(0,weight=1)

        #-------Attributes---------
        self.video_path = 0
        self.config = Tracker.CONFIG
        self.tracking_type = tk.StringVar(self, "face")
        self.tracking_type.trace("w",self.setTrackingType)


        #--------Widgets------------
        self.lbl_source = tk.Label(self, text="Source de la vidéo", font=("", 12, "bold"))
        self.lbl_webcam_info = tk.Label(self, text="(appuyer sur 📷 pour la webcam)")
        self.lbl_video_path = tk.Label(self, text="Webcam", font=('Helvetica', 15, "bold"), background="white")
        self.lbl_loading = tk.Label(self, text="Chargement ...")
        self.lbl_tracking_type = tk.Label(self, text="Choisir le mode de détection :")
        self.lbl_detection_rate = tk.Label(self, text="Nombre de frames entre chaque detection :")
        
        self.btn_browse = tk.Button(self, text="Chercher un fichier vidéo", command=self.browse_files)
        self.btn_choose_webcam = tk.Button(self, text="📷", font=("Helvetica", 14), command=self.choose_webcam)
        Hovertip(self.btn_choose_webcam, "Choisir la Webcam comme source video")
        self.btn_start = tk.Button(self, text="Lancer le tracking", background="#0052EA", foreground="white", 
        font=("",12, "bold"), command = self.launch_tracking)

        self.om_tracking_type = tk.OptionMenu(self, self.tracking_type, "face", "person")

        self.scl_detection_rate = tk.Scale(self, from_=30, to=200, orient=tk.HORIZONTAL)


        self.grid_widgets()
    
    def grid_widgets(self):
        self.lbl_source.grid(column=0, row=0, sticky="S")
        self.lbl_webcam_info.grid(row=1, sticky="N")
        self.lbl_video_path.grid(column=1, row=0)
        self.lbl_tracking_type.grid(column=0, row=2, pady=(10,0), sticky="S")
        self.lbl_detection_rate.grid(column=1, row=2, pady=(10,0), sticky="S")
        
        self.btn_browse.grid(column=1, row=1, padx=5, sticky="E")
        self.btn_choose_webcam.grid(column=2, row=1, padx=5)
        self.btn_start.grid(column=0, row=10, columnspan=3, pady=15)

        self.om_tracking_type.grid(column=0, row=3)
        self.scl_detection_rate.grid(column=1, row=3)
    
    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir = ".",
                                          title = "Select a File",
                                          filetypes = (("MP4","*.mp4"),("AVI",
                                                        "*.avi"), 
                                                        ("webp","*.wepb"),
                                                       ("all files",
                                                        "*.*")))
      
        self.config["VIDEO_PATH"] = filename
        # Change label contents
        self.lbl_video_path.configure(text = os.path.split(filename)[1])
    
    def choose_webcam(self):
        self.config["VIDEO_PATH"] = 0
        self.lbl_video_path.configure(text = "Webcam")
        
    def launch_tracking(self):
        self.config["DETECTION_RATE"] = int(self.scl_detection_rate.get())
        self.lbl_loading.grid(row=13, column=0, columnspan=3)
        tracking_loop(self.config, self.lbl_loading.grid_forget)
    
    def setTrackingType(self, *args):
        self.config["TRACKING_TYPE"] = self.tracking_type.get()
        
    