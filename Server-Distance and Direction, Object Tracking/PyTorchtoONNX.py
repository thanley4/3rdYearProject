import torch
import torchvision
import torch.onnx

model = torch.load('best.pt')

x = torch.rand()

torch_out = torch.onnx._export(model, x, "best.onnx", export_params=True)
