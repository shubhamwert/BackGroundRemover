import albumentations as A
from albumentations.pytorch import ToTensorV2
from PIL import Image
import numpy as np
import torchvision.utils  as U

from Parameter import image_height,image_width



class ImageLoader():
    def __init__(self):
        self.transform=A.Compose(
                                [
                                    
                                    A.Resize(height=image_height,width=image_width),
                                    A.Normalize(
                                    mean=[0.0,0.0,0.0],
                                    std=[1.0,1.0,1.0],
                                    max_pixel_value=255.0


                                    ),
                                    ToTensorV2()
                                    ])
    # def preprocess(self):
    
    def process(self,image=None,PATH_IMAGE=None):
        if PATH_IMAGE is not None:    
            image=np.array(Image.open(PATH_IMAGE).convert("RGB"))/255
        if image is None:
            raise "Error Image and Path both cannt be None"
        image=image
        aug=self.transform(image=image)
        
        return aug['image'],image