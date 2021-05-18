
import torch
import torchvision
import os

import torch.nn as nn
import torchvision.transforms.functional as TF
from Parameter import *







def load_checkpoint(c,model):
  print("loading_model...")
  model.load_state_dict(c["state_dict"])

class DoubleConv(nn.Module):
  def __init__(self,in_channels,out_channels):
    super(DoubleConv,self).__init__()
    self.conv = nn.Sequential(
            nn.Conv2d(in_channels,out_channels,3,1,1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channels,out_channels,3,1,1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            
    )
  def forward(self,X):
    return self.conv(X)
class UNET(nn.Module):
  def __init__(self,in_c,o_c=1,features=[64,128,256,512]):
    super(UNET,self).__init__()
    self.downs=nn.ModuleList(



    )
    self.ups=nn.ModuleList(
                                


    )
    self.pool=nn.MaxPool2d(kernel_size=2,stride=2)
    for f in features:
      self.downs.append(DoubleConv(in_c,f))
      in_c=f
    for f in reversed(features):
      self.ups.append(
                        nn.ConvTranspose2d(f*2,f,kernel_size=2,stride=2)
      )
      self.ups.append(DoubleConv(f*2,f))
      in_c=f
    self.bottleneck=DoubleConv(features[-1],features[-1]*2)
    self.final_conv=nn.Conv2d(features[0],o_c,kernel_size=1)
  def forward(self,X):
    
    skip_connections=[]
    for down in self.downs:
      X=down(X)
      skip_connections.append(X)
      X=self.pool(X)
    X=self.bottleneck(X)
    skip_connections=skip_connections[::-1]
    for idx in range(0,len(self.ups),2):
      X=self.ups[idx](X)
      skip_connection=skip_connections[idx//2]
      if X.shape!=skip_connection.shape:
        X=TF.resize(X,size=skip_connection.shape[2:])
      c=torch.cat((skip_connection,X),dim=1)
      X=self.ups[idx+1](c)
    return self.final_conv(X)


#Choose input divisble by 16


def createModel(PATH):
  
    model=UNET(in_c=3,o_c=1).to(device)
    model = torch.load(PATH,map_location=torch.device(device))
    model.to(device)
    model.eval()
    print("USING ",device)
    return model

def predict(x,model):
    with torch.no_grad():
      x=x.to(device)
      preds=torch.sigmoid(model(x))
      preds=(preds>PROB).float()
    return preds  
#   torchvision.utils.save_image(preds,"test/Images/pred_{}.png".format('r'))

