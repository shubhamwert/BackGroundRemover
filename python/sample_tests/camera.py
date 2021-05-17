from UNET import *
import cv2
import numpy as np
from ImageLoader import ImageLoader
from Parameter import *
model=createModel(PATH_MODEL)
model.eval()


image=cv2.imread('sample_backgrounds/index.jpeg')
image=cv2.resize(image,[640,480])
cap = cv2.VideoCapture(0)
I=ImageLoader()

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    if frame is None:
        continue
    X,_=I.process(image=frame.copy())
    mask=predict(X.unsqueeze(0),model)
    mask=mask.squeeze(0).squeeze(0).detach().cpu().numpy().copy()
    mask=cv2.resize(mask,[frame.shape[1],frame.shape[0]])
    mask=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    out = np.where(mask==[1.0,1.0,1.0], frame, image)

    cv2.imshow('frame',out)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()