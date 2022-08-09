import tkinter as tk
import tkinter.font as tkFont

from GUI.Window import MainWindow
import platform

if platform.system()=="Windows":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)


        
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("700x300")
    root.resizable(0,0)
    root.title("Enov Tracking System")
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(size=11)

    main = MainWindow(root)
    main.pack(fill="both", expand=True)

    root.mainloop()