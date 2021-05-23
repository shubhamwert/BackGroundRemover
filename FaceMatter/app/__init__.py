
from flask import Flask,Request
from FaceMat.ImageLoader import ImageLoader
from FaceMat.Parameter import *

from secrets import *
import numpy as np
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


#Load Model and Image Loader
model=createModel('model/m_2.pth')
image_processor=ImageLoader()
model.eval()



def getImage(filename):
    img_tensor,img=image_processor.process(PATH_IMAGE='U_FOLDER/{}'.format(filename))

    mask=predict(img_tensor.unsqueeze(0),model)

    mask=mask.squeeze(0).squeeze(0).detach().cpu().numpy().copy()
    face = np.where(mask==[1.0,1.0,1.0], mask, img)
    background= np.where(mask==[0.0,0.0,0.0], mask, img)
    return face,background