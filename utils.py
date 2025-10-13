import torch
import numpy as np
from model import LSTMForecast

def generate_forecast(sequence, n_steps=5):
    model = LSTMForecast()
    model.eval()

    # Simulate trained weights (placeholder)
    dummy_input = torch.randn(1, len(sequence), 1)
    with torch.no_grad():
        pred = model(dummy_input)

    return pred.squeeze().tolist()
