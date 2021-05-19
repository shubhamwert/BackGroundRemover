from io import DEFAULT_BUFFER_SIZE
import torch.cuda as tc
PATH_MODEL='model/model_full_unetv4.pth'
device="cuda" if tc.is_available() else "cpu"
PROB=0.6
DEFAULT_BG_PATH='sample_tests/sample_backgrounds/'