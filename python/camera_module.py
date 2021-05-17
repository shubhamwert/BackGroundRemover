from albumentations.augmentations.utils import read_bgr_image
from UNET import *
import cv2
import numpy as np
from ImageLoader import ImageLoader







class Camera:
    def __init__(self,PATH_MODEL,bg_path:None) -> None:
       self.model=createModel(PATH_MODEL)
       self.cap=cv2.VideoCapture(0)
       self.bg_path=bg_path
       self.I=ImageLoader()
    def capture(self,image):
        ret,frame=self.cap.read()
        assert image.shape ==frame.shape

        frame=cv2.flip(frame,1)
        if frame is None:
            return None,2
        X,_=self.I.process(image=frame.copy())
        mask=predict(X.unsqueeze(0),self.model)
        mask=mask.squeeze(0).squeeze(0).detach().cpu().numpy().copy()
        mask=cv2.resize(mask,[frame.shape[1],frame.shape[0]])
        mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
        out = np.where(mask==[1.0,1.0,1.0], frame, image)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            return None,0
        return out,1        
    def setbg(self,bg_path:None):
        if bg_path is None:
            return None
        else:
            self.bg_path=bg_path
            return 0

    def getbg(self,shape):
        if self.bg_path is None:
            return np.zeros(shape)
        else:

            image=cv2.imread(self.bg_path)
            image=cv2.resize(image,shape)
            return image
    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
    def run(self,stop_condition=True):

        bg_image=self.getbg([640,480])
        while stop_condition:
            out,response=self.capture(bg_image)
            
            if response==0:
                break
            else:
                if response==2:
                    continue

            cv2.imshow("Image",out)

        return 0

def main():
    C=Camera(PATH_MODEL,'sample_tests/sample_backgrounds/index.jpeg')
    C.run()
if __name__ == "__main__":
    main()