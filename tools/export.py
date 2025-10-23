# tools/export.py — TorchScript + ONNX export
import torch, pathlib
from app.model import model

OUT = pathlib.Path('exports'); OUT.mkdir(exist_ok=True)
dummy = torch.zeros(1, 16)  # TODO: edit per model if needed

ts = torch.jit.trace(model, dummy)
ts.save(str(OUT/'model_ts.pt'))

try:
    torch.onnx.export(model, dummy, str(OUT/'model.onnx'),
                      input_names=['input'], output_names=['output'],
                      opset_version=17, do_constant_folding=True)
    print('Exported ONNX')
except Exception as e:
    print('ONNX export failed:', e)
