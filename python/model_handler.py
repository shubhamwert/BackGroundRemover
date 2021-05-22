from utils import onnx_converter
import onnxruntime
import Parameter
import torch
from UNET import *
import numpy as np
def CreateModel(PATH="RANDOM"):
    '''Path is dummy variable kept for compatibility'''
    ort_session = onnxruntime.InferenceSession(Parameter.onnx_path)
    return ort_session

def verifyOnnx():
    import onnx

    onnx_model = onnx.load(Parameter.onnx_path)
    onnx.checker.check_model(onnx_model)
def predict(X,ort_session):
    ort_inputs = {ort_session.get_inputs()[0].name: X.numpy()}
    ort_outs = ort_session.run(None, ort_inputs)
    mask = ort_outs[0]
    mask[mask>0]=1
    return mask

def CreateOnxx(PATH):
    model=createModel(PATH)
    X=torch.randn([1,3,Parameter.image_height,Parameter.image_width],requires_grad=True).to(Parameter.device)
    onnx_converter.converter(model=model,x=X)
    p=onnx_converter.verify(Parameter.onnx_path)
    print(p)

    