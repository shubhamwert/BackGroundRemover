from io import DEFAULT_BUFFER_SIZE
import torch.cuda as tc
PATH_MODEL='model/m_2.pth'
device="cuda" if tc.is_available() else "cpu"
PROB=0.5
DEFAULT_BG_PATH='sample_tests/sample_backgrounds/'
onnx_path="model/model.onnx"
image_height=160
image_width=240

