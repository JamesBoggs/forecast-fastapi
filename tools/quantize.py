# tools/quantize.py — dynamic quant for Linear/LSTM-heavy nets
import torch
from app.model import model
q = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
num_params = sum(p.numel() for p in q.parameters())
print({'quantized_params': int(num_params)})
