import torch.cuda as tc
PATH_MODEL='model/model_full_unetv4.pth'
device="cuda" if tc.is_available() else "cpu"
