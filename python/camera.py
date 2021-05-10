from UNET import *
import cv2
from ImageLoader import ImageLoader
model=createModel('model/model_full_unetv9.pth')
model.eval()



cap = cv2.VideoCapture(0)
I=ImageLoader()

while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    if frame is None:
        continue
    X,_=I.process(image=frame)
    mask=predict(X.unsqueeze(0),model)
    mask=mask.squeeze(0).squeeze(0).detach().cpu().numpy()
    # cv2.imshow('Image',frame)
    cv2.imshow('mask',mask)
    
    # masked=cv2.bitwise_and(frame,frame,mask=mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()