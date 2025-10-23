# eval.py — deterministic OOS evaluation skeleton (fill in later)
import os, torch, random, numpy as np
torch.use_deterministic_algorithms(True)
torch.manual_seed(1337); random.seed(1337); np.random.seed(1337)

def main():
    print({'metric':'MAPE','value': 0.0, 'note': 'fill in dataset + split + baseline'})

if __name__ == '__main__':
    main()
