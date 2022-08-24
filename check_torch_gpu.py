import torch

if torch.cuda.is_available():
    print("Torch is using GPU!")
else:
    print("Torch is using CPU!")