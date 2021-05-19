from Parameter import PATH_MODEL,DEFAULT_BG_PATH
import tkinter as tk
import cv2
from PIL import ImageTk
from PIL import Image
import threading
from camera_module import Camera
from UNET import *
import numpy as np
class VideoApp:
    def __init__(self) -> None:
        self.cam=Camera(PATH_MODEL)
        # self.output_path=outputPath
        self.thread=None
        self.stopEvent=None
        self.current_bg=0
        self.root=tk.Tk()
        self.panel=None
        
        self.bg_list=self.getImageList(DEFAULT_BG_PATH)
        print(self.bg_list)
        btn = tk.Button(self.root, text="Change BG",
			command=self.change_bg)
        btn.pack(side="bottom", fill="both", expand="yes", padx=10,
			pady=10)
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_title("Video")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    def videoLoop(self):
            bg_image=self.cam.getbg([480,640])
            # print(bg_image.shape)
            while not self.stopEvent.is_set():
                    if self.cam.bgupdated:
                        bg_image=self.cam.getbg([640,480])
                        # cv2.imshow("blah",bg_image)
                        self.cam.bgupdated=False
                    frame,response = self.cam.capture(bg_image)
                    if response==0:
                        break
                    else:
                        if response==2:
                            continue


                    image = Image.fromarray(frame.astype(np.uint8))
                    image = ImageTk.PhotoImage(image)
            
                    # if the panel is not None, we need to initialize it
                    if self.panel is None:
                        self.panel = tk.Label(image=image)
                        self.panel.image = image
                        self.panel.pack(side="left", padx=10, pady=10)
            
                    # otherwise, simply update the panel
                    else:
                        self.panel.configure(image=image)
                        self.panel.image = image
    def change_bg(self):
        print('bg pth updated')
        self.current_bg+=1
        if self.current_bg>len(self.bg_list):
            self.current_bg=0
        self.cam.setbg(bg_path=self.bg_list[self.current_bg])
        self.cam.bgupdated=True
    def onClose(self):
        self.cam.close()
        self.root.destroy()
    def getImageList(self,path):
        files=[]
        for r, d, f in os.walk(path):
            for file in f:
                if '.jpg' in file or '.jpeg' in file:
                    files.append(os.path.join(r, file))
        return files

def main():
    C=VideoApp()
    C.root.mainloop()
if __name__ == "__main__":
    main()